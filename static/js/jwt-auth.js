/**
 * JWT Authentication Helper
 */

class JWTAuth {
    constructor() {
        this.baseURL = window.location.origin;
        this.tokenKey = 'access_token';
        this.refreshKey = 'refresh_token';
    }

    // Get stored token
    getToken() {
        return localStorage.getItem(this.tokenKey);
    }

    // Get refresh token
    getRefreshToken() {
        return localStorage.getItem(this.refreshKey);
    }

    // Store tokens
    setTokens(accessToken, refreshToken) {
        localStorage.setItem(this.tokenKey, accessToken);
        localStorage.setItem(this.refreshKey, refreshToken);
    }

    // Clear tokens
    clearTokens() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.refreshKey);
        localStorage.removeItem('user');
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.getToken();
    }

    // Get authorization headers
    getAuthHeaders() {
        const token = this.getToken();
        return token ? {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        } : {
            'Content-Type': 'application/json'
        };
    }

    // Refresh access token
    async refreshToken() {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) return false;

        try {
            const response = await fetch(`${this.baseURL}/accounts/api/auth/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem(this.tokenKey, data.access);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
        }

        this.clearTokens();
        return false;
    }

    // Make authenticated API request
    async apiRequest(url, options = {}) {
        const headers = this.getAuthHeaders();
        
        let response = await fetch(url, {
            ...options,
            headers: { ...headers, ...options.headers }
        });

        // If token expired, try to refresh
        if (response.status === 401) {
            const refreshed = await this.refreshToken();
            if (refreshed) {
                const newHeaders = this.getAuthHeaders();
                response = await fetch(url, {
                    ...options,
                    headers: { ...newHeaders, ...options.headers }
                });
            } else {
                window.location.href = '/accounts/api/auth/login/';
                return null;
            }
        }

        return response;
    }

    // Login
    async login(email, password) {
        try {
            const response = await fetch(`${this.baseURL}/accounts/api/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.setTokens(data.access, data.refresh);
                localStorage.setItem('user', JSON.stringify(data.user));
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Register
    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/accounts/api/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                this.setTokens(data.access, data.refresh);
                localStorage.setItem('user', JSON.stringify(data.user));
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    // Logout
    logout() {
        this.clearTokens();
        window.location.href = '/';
    }

    // Get current user
    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }
}

// Global instance
window.jwtAuth = new JWTAuth();

// Auto-redirect if not authenticated on protected pages
document.addEventListener('DOMContentLoaded', function() {
    const protectedPaths = ['/core/', '/dashboard/', '/profile/'];
    const currentPath = window.location.pathname;
    
    if (protectedPaths.some(path => currentPath.startsWith(path))) {
        if (!jwtAuth.isAuthenticated()) {
            window.location.href = '/templates/auth/jwt_login.html';
        }
    }
});