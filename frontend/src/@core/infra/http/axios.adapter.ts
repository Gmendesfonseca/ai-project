import axios from 'axios';
import { MINUTE_IN_MILLISECONDS } from '@/utils/constants';
import type { AxiosInstance, AxiosResponse } from 'axios';
import type {
  Get,
  Post,
  Patch,
  Put,
  Delete,
  IResponse,
  IHttpClient,
  IApiClientConfig,
} from '../../domain/ports/http-client.port';

interface ErrorWithResponse {
  response?: {
    data: unknown;
    status: number;
  };
  request?: unknown;
  message?: string;
  toJSON?: () => unknown;
}

export class AxiosHttpAdapter implements IHttpClient {
  private instance: AxiosInstance;

  constructor(axiosInstance?: AxiosInstance, config?: IApiClientConfig) {
    this.instance =
      axiosInstance ||
      axios.create({
        baseURL: config?.baseURL || import.meta.env.VITE_API_URL || '/api',
        timeout: config?.timeout || 2 * MINUTE_IN_MILLISECONDS,
        headers: {
          'Content-Type': 'application/json',
          ...config?.headers,
        },
      });
  }

  public async get<R>({
    url,
    params,
    headers,
  }: Get): Promise<IResponse<R | null>> {
    try {
      const response = await this.instance.get<R>(url, { params, headers });
      return this.toOutput<R>(response);
    } catch (error) {
      return this.handleError(error);
    }
  }

  public async post<R>({
    url,
    payload,
    headers,
  }: Post): Promise<IResponse<R | null>> {
    try {
      const response = await this.instance.post<R>(url, payload, { headers });
      return this.toOutput<R>(response);
    } catch (error) {
      return this.handleError(error);
    }
  }

  public async patch<R>({
    url,
    headers,
    payload,
  }: Patch): Promise<IResponse<R | null>> {
    try {
      const response = await this.instance.patch<R>(url, payload, { headers });
      return this.toOutput<R>(response);
    } catch (error) {
      return this.handleError(error);
    }
  }

  public async put<R>({
    url,
    payload,
    headers,
  }: Put): Promise<IResponse<R | null>> {
    try {
      const response = await this.instance.put<R>(url, payload, { headers });
      return this.toOutput<R>(response);
    } catch (error) {
      return this.handleError(error);
    }
  }

  public async delete<R>({
    url,
    params,
    headers,
  }: Delete): Promise<IResponse<R | null>> {
    try {
      const response = await this.instance.delete<R>(url, { params, headers });
      return this.toOutput<R>(response);
    } catch (error) {
      return this.handleError(error);
    }
  }

  private handleError(error: unknown): IResponse<null> {
    const err = error as ErrorWithResponse;
    if (err.response) {
      console.error(
        `AxiosHttpClientAdapter: Response Error: ${
          err.message
        }, Data: ${JSON.stringify(err.response.data)}, status -> ${
          err.response.status
        }`,
      );
    } else if (err.request) {
      console.error(
        `AxiosHttpClientAdapter: Request Error: ${
          err.message
        }, Data: ${JSON.stringify(err.toJSON?.())}`,
      );
    } else {
      console.error(`AxiosHttpClientAdapter: Error: ${err.message}`);
    }
    return {
      data: null,
      status: err.response?.status || 500,
      statusText: err.message || 'Internal Server Error',
      headers: {},
    };
  }

  private toOutput<T>(response: AxiosResponse<T>): IResponse<T | null> {
    return {
      data: response.data || null,
      status: response.status,
      statusText: response.statusText,
      headers: response.headers as Record<string, string>,
    };
  }
}
