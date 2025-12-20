import ApiService from './ApiService'

class NobelService {
    async getNobelPrizes(options = {}) {
        const {
            offset = 0,
            limit = 20,
            sort = 'asc',
            nobelPrizeYear,
            yearTo,
            nobelPrizeCategory
        } = options

        const params = {
            offset,
            limit,
            sort
        }

        if (nobelPrizeYear) params.nobelPrizeYear = nobelPrizeYear
        if (yearTo) params.yearTo = yearTo
        if (nobelPrizeCategory) params.nobelPrizeCategory = nobelPrizeCategory

        return await ApiService.get('/nobelPrizes', params)
    }

    async getLaureates(options = {}) {
        const {
            offset = 0,
            limit = 20,
            sort = 'asc',
            name,
            gender,
            nobelPrizeYear,
            nobelPrizeCategory
        } = options

        const params = {
            offset,
            limit,
            sort
        }

        if (name) params.name = name
        if (gender) params.gender = gender
        if (nobelPrizeYear) params.nobelPrizeYear = nobelPrizeYear
        if (nobelPrizeCategory) params.nobelPrizeCategory = nobelPrizeCategory

        return await ApiService.get('/laureates', params)
    }
}

export default new NobelService()