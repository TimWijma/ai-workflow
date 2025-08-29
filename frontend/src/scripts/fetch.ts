/**
 * Fetch wrapper
 *
 * Example usage:
 * Fetch.get<ResponseType>("url", {search: "param"})
 *      .then((data) => { ... }
 *      .catch((error) => { ... }
 *
 * When you have to wait for a response, use await Fetch.method()
 *
 * Params parameter are for query string parameters:
 * {search: "param", page: 1} will result in url?search=param&page=1
 *
 * Body parameter is for the body of the request.
 * You can pass an already stringified JSON object or a JS object.
 */
export class Fetch {
  static async get<T = any>(url: string, params: any = {}): Promise<T> {
    let apiUrl = Fetch.createUrl(url, params)
    return fetch(apiUrl, {
      method: 'GET',
    }).then(Fetch.responseHandler)
  }

  static async post<T = any>(url: string, body: any = {}, params: any = {}): Promise<T> {
    let apiUrl = Fetch.createUrl(url, params)

    const requestBody = typeof body === 'string' ? body : JSON.stringify(body)

    return fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
      body: requestBody,
    }).then(Fetch.responseHandler)
  }

  static async put<T = any>(url: string, body: any = {}, params: any = {}): Promise<T> {
    let apiUrl = Fetch.createUrl(url, params)

    const requestBody = typeof body === 'string' ? body : JSON.stringify(body)

    return fetch(apiUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
      body: requestBody,
    }).then(Fetch.responseHandler)
  }

  static async delete<T = any>(url: string, params: any = {}): Promise<T> {
    let apiUrl = Fetch.createUrl(url, params)
    return fetch(apiUrl, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
    }).then(Fetch.responseHandler)
  }

  private static async responseHandler(response: Response) {
    if (!response.ok) {
      let responseError = {
        status: response.status,
        statusText: response.statusText,
        message: '',
        url: response.url,
      }

      const text = await response.text()

      if (text) {
        try {
          responseError.message = JSON.parse(text)
        } catch (error) {
          responseError.message = text
        }
      }

      return Promise.reject(responseError)
    }

    return response.text().then((text) => {
      if (!text) null

      try {
        return JSON.parse(text)
      } catch (error) {
        return text
      }
    })
  }

  private static createUrl(url: string, params: any = {}) {
    let apiUrl = new URL(url)
    apiUrl.search = new URLSearchParams(params).toString()
    return apiUrl
  }
}
