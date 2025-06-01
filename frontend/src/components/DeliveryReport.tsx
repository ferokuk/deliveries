import React, {useEffect, useState} from 'react';
import {
    Box,
    Container,
    Paper,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
    CircularProgress,
    Pagination,
    type SelectChangeEvent,
    IconButton,
    Menu,
    Avatar
} from '@mui/material';
import {DatePicker, LocalizationProvider} from '@mui/x-date-pickers';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts';
import {format, parseISO} from 'date-fns';
import {ru} from 'date-fns/locale';
import {AdapterDateFns} from "@mui/x-date-pickers/AdapterDateFns";
import api from "../api/api.ts";
import {logout} from "../api/auth.ts";

interface Delivery {
    id: number;
    departure_datetime: string;
    distance_km: string;
    transport_model: { plate_number: string };
    services: Array<{ id: number; name: string }>;
    cargo_type: { id: number; name: string };
}

interface FilterOption {
    id: number;
    name: string;
    results: [];
}

interface ChartData {
    day: string;
    count: number;
}

interface PaginationResponse<T> {
    count: number;
    results: T[];
}

type DeliveryPagination = PaginationResponse<Delivery>;
type FilterPagination = PaginationResponse<FilterOption>;

interface Props {
    onLogout: () => void;
}

const DeliveryReport: React.FC<Props> = ({onLogout}) => {
    const [paginationData, setPaginationData] = useState<DeliveryPagination>({
        count: 0,
        results: []
    });
    const [cargoTypes, setCargoTypes] = useState<FilterOption[]>([]);
    const [serviceTypes, setServiceTypes] = useState<FilterOption[]>([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);
    const [chartData, setChartData] = useState<ChartData[]>([]);
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const [filters, setFilters] = useState({
        startDate: null as Date | null,
        endDate: null as Date | null,
        cargoType: undefined as string | undefined,
        serviceType: undefined as string | undefined,
        ordering: '-departure_datetime'
    });
    useEffect(() => {
        setPage(1);
    }, [filters]);
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const params = {
                    page,
                    page_size: pageSize,
                    ordering: filters.ordering,
                    ...(filters.startDate && {
                        departure_datetime__gte: format(filters.startDate, 'yyyy-MM-dd')
                    }),
                    ...(filters.endDate && {
                        departure_datetime__lte: format(filters.endDate, 'yyyy-MM-dd')
                    }),
                    ...(filters.cargoType && {cargo_type: filters.cargoType}),
                    ...(filters.serviceType && {services: filters.serviceType}),
                };

                const countRes = await api.get<DeliveryPagination>(`/deliveries/`, {
                    params: {...params, page: 1, page_size: 1}  // Минимальная нагрузка
                });

                const total = countRes.data.count;
                const totalPages = Math.ceil(total / pageSize);

                // Если текущая страница превышает, скидываем
                if (page > totalPages && totalPages > 0) {
                    setPage(totalPages);
                    return;
                }
                const [deliveriesRes, chartRes, cargoRes, servicesRes] = await Promise.all([
                    api.get<DeliveryPagination>(`/deliveries/`, {
                        params
                    }).catch(e => {
                        if (e.response?.status === 401) {
                            onLogout();
                        }
                        console.error('Delivery error:', e);
                        return {data: {count: 0, results: []}};
                    }),

                    api.get<ChartData[]>(`/deliveries/summary/`, {
                        params
                    }).catch(e => {
                        console.error(e)
                        return {data: []};
                    }),

                    api.get<FilterPagination>(`/cargo/`, {}).catch(() => ({
                        data: {
                            count: 0,
                            results: []
                        } as FilterPagination
                    })),

                    api.get<FilterPagination>(`/services/`, {}).catch(() => ({
                        data: {
                            count: 0,
                            results: []
                        } as FilterPagination
                    }))
                ]);


                setPaginationData({
                    count: deliveriesRes.data.count,
                    results: deliveriesRes.data.results
                });
                setChartData(chartRes.data);
                setCargoTypes(cargoRes.data.results);
                setServiceTypes(servicesRes.data.results);

            } catch (err) {
                console.error('General error:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();

    }, [page, pageSize, filters, onLogout]);

    const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
        setPage(value);
    };

    const handlePageSizeChange = (e: SelectChangeEvent) => {
        setPageSize(Number(e.target.value));
        setPage(1);
    };

    return (
        <Container maxWidth="xl" sx={{mt: 4, mb: 4, position: 'relative'}}>
            <Box sx={{position: 'absolute', top: 16, right: 16}}>
                <IconButton onClick={handleMenuOpen}>
                    <Avatar sx={{bgcolor: '#bb86fc'}}>U</Avatar>
                </IconButton>
                <Menu
                    anchorEl={anchorEl}
                    open={open}
                    onClose={handleMenuClose}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'right',
                    }}
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'right',
                    }}
                >
                    <MenuItem
                        onClick={async () => {
                            handleMenuClose();
                            try {
                                await logout();
                                onLogout();
                            } catch (e) {
                                console.error(e);
                            }
                        }}
                    >
                        Выйти
                    </MenuItem>
                </Menu>
            </Box>
            {loading && (
                <Box
                    sx={{
                        position: 'fixed', // было absolute
                        top: 0,
                        left: 0,
                        width: '100vw',
                        height: '100vh',
                        bgcolor: 'rgba(117,168,250,0.11)', // фиолетовый с прозрачностью
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        zIndex: 1300 // поверх всего
                    }}
                >
                    <CircularProgress color="secondary" sx={{color: '#bb86fc'}}/>
                </Box>
            )}
            <Box sx={{display: 'flex', gap: 3, mb: 3, flexWrap: 'wrap'}}>
                <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ru}>
                    <DatePicker
                        label="Начальная дата"
                        value={filters.startDate}
                        onChange={(date) => setFilters({
                            ...filters,
                            startDate: date,
                            endDate: date ? filters.endDate : null
                        })}
                        format={'dd.MM.yyyy'}
                        sx={{width: 200}}
                    />
                    <DatePicker
                        label="Конечная дата"
                        value={filters.endDate}
                        onChange={(date) => setFilters({...filters, endDate: date})}
                        format={'dd.MM.yyyy'}
                        sx={{width: 200}}
                        disabled={!filters.startDate}
                    />
                </LocalizationProvider>
                <FormControl sx={{width: 200}}>
                    <InputLabel>Тип груза</InputLabel>
                    <Select
                        value={filters.cargoType || ''}
                        onChange={e => setFilters({
                            ...filters,
                            cargoType: e.target.value || undefined
                        })}
                    >
                        <MenuItem value="">Все</MenuItem>
                        {cargoTypes.map(cargo => (
                            <MenuItem key={cargo.id} value={cargo.id.toString()}>
                                {cargo.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <FormControl sx={{width: 200}}>
                    <InputLabel>Тип услуги</InputLabel>
                    <Select
                        value={filters.serviceType || ''}
                        onChange={e => setFilters({
                            ...filters,
                            serviceType: e.target.value || undefined
                        })}
                    >
                        <MenuItem value="">Все</MenuItem>
                        {serviceTypes.map(service => (
                            <MenuItem key={service.id} value={service.id.toString()}>
                                {service.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <FormControl sx={{width: 200}}>
                    <InputLabel>Сортировка</InputLabel>
                    <Select
                        value={filters.ordering}
                        label="Сортировка"
                        onChange={e => setFilters({...filters, ordering: e.target.value})}
                    >
                        <MenuItem value="-departure_datetime">Сначала новые</MenuItem>
                        <MenuItem value="departure_datetime">Сначала старые</MenuItem>
                        <MenuItem value="-distance_km">Дистанция по убыванию</MenuItem>
                        <MenuItem value="distance_km">Дистанция по возрастанию</MenuItem>
                    </Select>
                </FormControl>
            </Box>

            {/* График */}
            <Paper sx={{mb: 4, p: 3, borderRadius: 4}}>
                <Typography variant="h6" gutterBottom sx={{mb: 3}}>
                    Количество доставок
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                    {chartData.length > 0 ? (
                        <LineChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#37474F"/>
                            <XAxis dataKey="day" stroke="#bb86fc" tickFormatter={
                                value => format(parseISO(value), 'MMM d ', {locale: ru})
                            }/>
                            <YAxis stroke="#bb86fc"/>
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#1e1e1e',
                                    border: 'none',
                                    borderRadius: 10,
                                }}
                                labelFormatter={(value) =>
                                    format(parseISO(value), 'd MMMM yyyy', {locale: ru})
                                }
                                formatter={(value) => [value, 'Количество доставок']}
                            />
                            <Line
                                type="monotone"
                                dataKey="count"
                                stroke="#bb86fc"
                                strokeWidth={2}
                                dot={{fill: '#03dac6', strokeWidth: 2}}
                                activeDot={{fill: '#0359da', strokeWidth: 2}}
                            />
                        </LineChart>
                    ) : (
                        <Box sx={{
                            height: '100%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}>
                            <Typography variant="body1">Нет данных для отображения</Typography>
                        </Box>
                    )}
                </ResponsiveContainer>
            </Paper>

            {/* Таблица */}
            <TableContainer component={Paper} sx={{borderRadius: 4}}>
                <Table>
                    <TableHead sx={{bgcolor: 'background.paper'}}>
                        <TableRow>
                            <TableCell style={{fontWeight: 'bold'}} align="center">Доставка</TableCell>
                            <TableCell style={{fontWeight: 'bold'}} align="center">Дата создания доставки</TableCell>
                            <TableCell style={{fontWeight: 'bold'}} align="center">Модель ТС</TableCell>
                            <TableCell style={{fontWeight: 'bold'}} align="center">Услуга</TableCell>
                            <TableCell style={{fontWeight: 'bold'}} align="center">Дистанция (км)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {paginationData.results?.length > 0 ? (
                            paginationData.results.map(d => (
                                <TableRow key={d.id}>
                                    <TableCell align="center">Доставка #{d.id}</TableCell>
                                    <TableCell align="center">
                                        {format(parseISO(d.departure_datetime), 'dd.MM.yyyy HH:mm')}
                                    </TableCell>
                                    <TableCell align="center">{d.transport_model.plate_number}</TableCell>
                                    <TableCell align="center">{d.services.map(s => s.name).join(', ')}</TableCell>
                                    <TableCell align="center">{parseFloat(d.distance_km).toFixed(2)}</TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={5} align="center">
                                    {loading ? 'Загрузка...' : 'Нет данных для отображения'}
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            <Box sx={{display: 'flex', justifyContent: 'space-between', mt: 2, alignItems: 'center'}}>
                <Pagination
                    count={Math.ceil(paginationData.count / pageSize)}
                    page={page}
                    onChange={handlePageChange}
                    color="primary"
                    showFirstButton
                    showLastButton
                />

                <FormControl sx={{width: 120, ml: 2}}>
                    <InputLabel>На странице</InputLabel>
                    <Select
                        value={pageSize.toString()}
                        label="На странице"
                        onChange={handlePageSizeChange}
                    >
                        <MenuItem value={10}>10</MenuItem>
                        <MenuItem value={25}>25</MenuItem>
                        <MenuItem value={50}>50</MenuItem>
                    </Select>
                </FormControl>
            </Box>
        </Container>
    );
};

export default DeliveryReport;
