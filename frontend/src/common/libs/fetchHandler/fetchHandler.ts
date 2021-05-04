import axios, { AxiosInstance, AxiosPromise, AxiosRequestConfig } from 'axios';
import { IDictionary } from '@/common/types/baseType';

type Response = IDictionary | string | IDictionary[];

export default class FetchHandler {
  public constructor(baseUrl?: string) {
    this.axios = axios.create({
      baseURL: baseUrl,
    });
  }

  public axios: AxiosInstance;

  private installed: boolean = false;

  public get(url: string, params?: IDictionary): AxiosPromise<Response> {
    const config: AxiosRequestConfig = { params: params || {} };

    return this.axios.get(url, config);
  }

  public get_original(url: string, config?: AxiosRequestConfig): AxiosPromise<Response> {
    return this.axios.get(url, config);
  }

  public post(url: string, data?: IDictionary, params?: IDictionary): AxiosPromise<Response> {
    const config: AxiosRequestConfig = { params: params || {} };
    return this.axios.post(url, data, config);
  }

  public post_original(url: string, data?: IDictionary,
                       config?: AxiosRequestConfig): AxiosPromise<Response> {
    return this.axios.post(url, data, config);
  }

  public put(url: string, data?: IDictionary, params?: IDictionary): AxiosPromise<Response> {
    const config: AxiosRequestConfig = { params: params || {} };
    return this.axios.put(url, data, config);
  }

  public delete(url: string, params?: IDictionary): AxiosPromise<Response> {
    const config: AxiosRequestConfig = { params: params || {} };
    return this.axios.delete(url, config);
  }

  public install(Vue: any) {
    if (this.installed) {
      return;
    }

    this.installed = true;

    const self = this;
    const properties = {
      $fetch: {
        get(): FetchHandler {
          return self;
        },
      },
    };
    Object.defineProperties(Vue.prototype, properties);
    Object.defineProperties(Vue, properties);
  }
}
