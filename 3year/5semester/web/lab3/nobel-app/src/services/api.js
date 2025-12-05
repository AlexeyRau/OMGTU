import axios from 'axios'

class ApiService {
    constructor() {
        this.baseURL = 'https://api.nobelprize.org/2.1'

        this.instance = axios.create({
            baseURL: this.baseURL,
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })

        this.instance.interceptors.response.use(
            response => response,
            error => {
                let errorMessage = 'Произошла ошибка при запросе к API'

                if (error.response) {
                    switch (error.response.status) {
                        case 400:
                            errorMessage = 'Некорректный запрос'
                            break
                        case 404:
                            errorMessage = 'Данные не найдены'
                            break
                        case 429:
                            errorMessage = 'Слишком много запросов. Попробуйте позже'
                            break
                        case 500:
                            errorMessage = 'Ошибка сервера'
                            break
                        default:
                            errorMessage = `Ошибка ${error.response.status}`
                    }
                } else if (error.request) {
                    errorMessage = 'Не удалось получить ответ от сервера. Проверьте подключение к интернету'
                } else {
                    errorMessage = error.message
                }

                console.error('API Error Details:', {
                    message: errorMessage,
                    url: error.config?.url,
                    method: error.config?.method
                })

                return Promise.reject(new Error(errorMessage))
            }
        )
    }

    async get(endpoint, params = {}) {
        try {
            const response = await this.instance.get(endpoint, { params })
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export default new ApiService()