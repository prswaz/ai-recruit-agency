import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkUser = async () => {
            const token = localStorage.getItem('token');
            console.log("AuthContext: Checking token:", token ? "Found" : "Missing");
            if (token) {
                try {
                    const response = await api.get('/auth/me');
                    console.log("AuthContext: User loaded:", response.data);
                    setUser(response.data);
                } catch (error) {
                    console.error("Auth check failed", error);
                    localStorage.removeItem('token');
                }
            }
            setLoading(false);
        };
        checkUser();
    }, []);

    const login = async (email, password) => {
        const response = await api.post('/auth/token', {
            email: email,
            password: password
        });

        const { access } = response.data;
        localStorage.setItem('token', access);

        // Get user details immediately
        const userResp = await api.get('/auth/me');
        setUser(userResp.data);
        return userResp.data;
    };

    const register = async (userData) => {
        await api.post('/auth/register', userData);
        // Auto login after register? Or require separate login. 
        // Let's forward to login for now.
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
