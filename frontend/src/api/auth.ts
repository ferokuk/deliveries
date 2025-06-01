import api from './api'; // Ваш настроенный Axios инстанс

// Типы данных

export interface AuthResponse {
    status: string;
    detail: string;
}

export interface LoginCredentials {
    username: string;
    password: string;
}

/**
 * Авторизация пользователя
 * @param credentials - Данные для входа
 * @returns Сообщение об успехе или неудаче
 */
export const login = async (
    credentials: LoginCredentials
): Promise<AuthResponse> => {
    try {

        const response = await api.post<AuthResponse>('/token/', credentials);
        return response.data;
    } catch (error: any) {
        const errorMessage = error.response?.data?.detail || 'Ошибка входа';
        console.error('Login error:', errorMessage);
        throw new Error(errorMessage);
    }
};

/**
 * Выход из аккаунта
 */
export const logout = async (): Promise<void> => {
    try {
        await api.post('/logout/');
    } catch (error: any) {
        const errorMessage = error.response?.data?.detail || 'Ошибка при выходе.';
        console.error('Logout error:', errorMessage);
        throw new Error(errorMessage);
    }
};

/**
 * Проверка авторизации пользователя
 * @returns Данные об успешном входе или null
 */
export const checkAuth = async (): Promise<any> => {
    try {
        const response = await api.get<AuthResponse>('/services/');
        return response.data;
    } catch (error: any) {
        if (error.response?.status === 401) {
            return null;
        }

        const errorMessage = error.response?.data?.detail || 'Auth check failed';
        console.error('Auth check error:', errorMessage);
        return null
    }
};

/**
 * Обновление токена (автоматически вызывается интерцептором)
 */
export const refreshToken = async (): Promise<void> => {
    try {
        await api.post('/token/refresh/');
    } catch (error: any) {
        const errorMessage = error.response?.data?.detail || 'Token refresh failed';
        console.error('Refresh error:', errorMessage);
        throw new Error('Сессия закончилась. Пожалуйста войдите заново.');
    }
};
