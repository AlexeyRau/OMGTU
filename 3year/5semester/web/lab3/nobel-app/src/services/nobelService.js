import api from './api'

class NobelService {
    async getLaureates(page = 0, limit = 10, filters = {}) {
        const params = {
            offset: page * limit,
            limit: limit,
            ...filters
        }

        Object.keys(params).forEach(key => {
            if (params[key] === '' || params[key] === null || params[key] === undefined) {
                delete params[key]
            }
        })

        return api.get('/laureates', params)
    }

    async getNobelPrizes(page = 0, limit = 10, filters = {}) {
        const params = {
            offset: page * limit,
            limit: limit,
            ...filters
        }

        Object.keys(params).forEach(key => {
            if (params[key] === '' || params[key] === null || params[key] === undefined) {
                delete params[key]
            }
        })

        return api.get('/nobelPrizes', params)
    }
}

export default new NobelService()