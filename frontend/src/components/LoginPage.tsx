import React, {useState} from 'react';
import {
    Box,
    Paper,
    TextField,
    Button,
    Typography,
    Alert,
    useTheme,
} from '@mui/material';
import {login} from "../api/auth.ts";

interface Props {
    onLogin: () => void;
}


const LoginPage: React.FC<Props> = ({onLogin}) => {
    const theme = useTheme();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            if (!username || !password) throw new Error('Введите логин и пароль');
            await login({username, password});
            onLogin();
        } catch (error: any) {
            setError(`Произошла ошибка при входе: ${error.message}`);
        }
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                bgcolor: 'background.default',
                p: 2, // Добавляем отступы по краям для мобильных устройств
            }}
        >
            <Paper
                elevation={3}
                sx={{
                    width: '100%',
                    maxWidth: 448, // Оптимальная ширина по Material Design 3
                    p: 4,
                    borderRadius: 4, // Более округлые углы
                    bgcolor: 'background.paper',
                    boxShadow: theme.shadows[6], // Более выраженная тень
                }}
            >
                <Typography
                    variant="h4"
                    component="h1"
                    sx={{
                        mb: 4,
                        fontWeight: 700,
                        textAlign: 'center',
                        color: 'text.primary',
                    }}
                >
                    Вход
                </Typography>

                <Box
                    component="form"
                    onSubmit={handleSubmit}
                    sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 2, // Используем системные отступы
                    }}
                >
                    <TextField
                        fullWidth
                        variant="outlined" // Более современный вариант
                        label="Логин"
                        InputProps={{
                            sx: {borderRadius: 2} // Скругление поля ввода
                        }}
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                    />

                    <TextField
                        fullWidth
                        variant="outlined"
                        type="password"
                        label="Пароль"
                        InputProps={{
                            sx: {borderRadius: 2}
                        }}
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    />

                    {error && (
                        <Alert
                            severity="error"
                            sx={{
                                mt: 1,
                                borderRadius: 2 // Скругление алерта
                            }}
                        >
                            {error}
                        </Alert>
                    )}

                    <Button
                        type="submit"
                        variant="contained"
                        size="large"
                        sx={{
                            mt: 2,
                            py: 1.5,
                            borderRadius: 2, // Скругление кнопки
                            fontSize: '1rem',
                            textTransform: 'none', // Убираем капс
                            fontWeight: 600,
                        }}
                    >
                        Продолжить
                    </Button>
                </Box>
            </Paper>
        </Box>
    );
};

export default LoginPage;
