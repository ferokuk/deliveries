import {useState, useEffect} from 'react';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import {ThemeProvider, createTheme, CssBaseline} from '@mui/material';
import LoginPage from './components/LoginPage';
import DeliveryReport from './components/DeliveryReport.tsx';
import {LocalizationProvider} from '@mui/x-date-pickers';
import {AdapterDateFns} from '@mui/x-date-pickers/AdapterDateFns';
import {checkAuth} from "./api/auth.ts";
// Ваша существующая тема с добавленными глобальными стилями
const darkTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {main: '#bb86fc'},
        secondary: {main: '#03dac6'},
        background: {default: '#121212', paper: '#1e1e1e'}
    },
    components: {
        MuiCssBaseline: {
            styleOverrides: {
                html: {
                    height: '100%',
                    margin: 0,
                    padding: 0,
                },
                body: {
                    height: '100%',
                    margin: 0,
                    padding: 0,
                    overflowX: 'hidden',
                },
                '#root': {
                    height: '100%',
                    minHeight: '100vh',
                    display: 'flex',
                    flexDirection: 'column',
                },
            },
        },
    },
});

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const check = async () => {
            try {
                const res = await checkAuth();
                setIsAuthenticated(!!res);
            } catch {
                setIsAuthenticated(false);
            }
        };
        check();
    }, []);


    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline/>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
                <Router>
                    <Routes>
                        <Route path="/login" element={
                            !isAuthenticated ? (
                                <LoginPage onLogin={() => setIsAuthenticated(true)}/>
                            ) : (
                                <Navigate to="/" replace/>
                            )
                        }/>
                        <Route path="/" element={
                            isAuthenticated ? (
                                <DeliveryReport onLogout={() => setIsAuthenticated(false)}/>
                            ) : (
                                <Navigate to="/login" replace/>
                            )
                        }/>
                    </Routes>
                </Router>
            </LocalizationProvider>
        </ThemeProvider>
    );
}

export default App;
