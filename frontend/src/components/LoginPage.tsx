import React, {useState} from 'react';
import {
    Box,
    Paper,
    TextField,
    Button,
    Typography,
    Alert,
    useTheme,
    CircularProgress, // 1. Импортируем спиннер
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
    const [loading, setLoading] = useState(false); // 2. Состояние загрузки

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true); // 3. Начинаем загрузку

        try {
            if (!username || !password) throw new Error('Введите логин и пароль');
            await login({username, password});
            onLogin();
        } catch (error: any) {
            setError(`Произошла ошибка при входе: ${error.message}`);
        } finally {
            setLoading(false); // 3. Останавливаем спиннер
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
                p: 2,
            }}
        >
            <Paper
                elevation={3}
                sx={{
                    width: '100%',
                    maxWidth: 448,
                    p: 4,
                    borderRadius: 4,
                    bgcolor: 'background.paper',
                    boxShadow: theme.shadows[6],
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
                        gap: 2,
                    }}
                >
                    <TextField
                        fullWidth
                        variant="outlined"
                        label="Логин"
                        InputProps={{
                            sx: {borderRadius: 2}
                        }}
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        disabled={loading} // Блокируем поля при загрузке
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
                        disabled={loading}
                    />

                    {error && (
                        <Alert
                            severity="error"
                            sx={{
                                mt: 1,
                                borderRadius: 2
                            }}
                        >
                            {error}
                        </Alert>
                    )}

                    <Button
                        type="submit"
                        variant="contained"
                        size="large"
                        disabled={loading} // Блокируем кнопку при загрузке
                        sx={{
                            mt: 2,
                            py: 1.5,
                            borderRadius: 2,
                            fontSize: '1rem',
                            textTransform: 'none',
                            fontWeight: 600,
                        }}
                    >
                        {loading
                            ? <CircularProgress size={24} /> // 4. Показ спиннера вместо текста
                            : 'Продолжить'
                        }
                    </Button>
                </Box>
            </Paper>
        </Box>
    );
};

export default LoginPage;
