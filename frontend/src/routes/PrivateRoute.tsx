import React from 'react';
import {Navigate} from 'react-router-dom';
import type { JSX } from 'react/jsx-runtime';

interface PrivateRouteProps {
    children: JSX.Element;
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({children}) => {
    const token = localStorage.getItem('token');
    return token ? children : <Navigate to="/login" replace/>;
};

export default PrivateRoute;
