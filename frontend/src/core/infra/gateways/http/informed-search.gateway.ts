import type { IHttpClient } from '@core/domain/ports/http-client.port';
import type {
  BaseOutput,
  HeuristicInput,
  InformedSearchGateway,
} from '@core/domain/gateway';

export class InformedSearchHttpGateway implements InformedSearchGateway {
  private readonly httpClient: IHttpClient;
  private readonly baseUrl = '/search/informed';

  constructor(httpClient: IHttpClient) {
    this.httpClient = httpClient;
  }

  async aStar(payload: HeuristicInput): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/a_star`,
    });
    return response.data;
  }

  async uniformCost(payload: HeuristicInput): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/uniform_cost`,
    });
    return response.data;
  }

  async greedy(payload: HeuristicInput): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/greedy`,
    });
    return response.data;
  }

  async idaStar(payload: HeuristicInput): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/ida_star`,
    });
    return response.data;
  }
}
