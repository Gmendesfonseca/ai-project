export interface Get {
  url: string;
  params?: Record<string, unknown>;
  headers?: Record<string, string>;
}

export interface Post {
  url: string;
  payload?: unknown;
  headers?: Record<string, string>;
}

export interface Put {
  url: string;
  payload?: unknown;
  headers?: Record<string, string>;
}

export interface Patch {
  url: string;
  payload?: unknown;
  headers?: Record<string, string>;
}

export interface Delete {
  url: string;
  params?: Record<string, unknown>;
  headers?: Record<string, string>;
}

export interface IRequest {
  url?: string;
  method?: string;
  data?: Record<string, unknown>;
  params?: Record<string, unknown>;
  headers: Record<string, string>;
}

export interface IResponse<T = unknown> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}

export interface IApiClientConfig {
  baseURL?: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export abstract class IHttpClient {
  abstract get<T>(options: Get): Promise<IResponse<T | null>>;
  abstract post<T>(options: Post): Promise<IResponse<T | null>>;
  abstract put<T>(options: Put): Promise<IResponse<T | null>>;
  abstract patch<T>(options: Patch): Promise<IResponse<T | null>>;
  abstract delete<T>(options: Delete): Promise<IResponse<T | null>>;
}
