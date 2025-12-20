import axios from 'axios'

class ApiService {
    constructor() {
        this.baseURL = 'https://api.nobelprize.org/2.1'

        this.apiClient = axios.create({
            baseURL: this.baseURL,
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json',
            }
        })
    }

    async get(endpoint, params = {}) {
        try {
            const response = await this.apiClient.get(endpoint, { params })
            return response.data
        } catch (error) {
            console.error('API Error:', error)
            throw error
        }
    }
}

export default new ApiService()