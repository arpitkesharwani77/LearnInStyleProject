const API_URL = 'http://localhost:8000/api';

export async function fetchAPI(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    if (token) {
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
        };
    }
    const response = await fetch(`${API_URL}${endpoint}`, options);
    return response.json();
}
