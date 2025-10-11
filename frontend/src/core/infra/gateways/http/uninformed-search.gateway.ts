import type { IHttpClient } from '@core/domain/ports/http-client.port';
import type {
  BaseInput,
  BaseOutput,
  DepthLimited,
  IterativeDeepening,
  UninformedSearchGateway,
} from '@core/domain/gateway';

export class UninformedSearchHttpGateway implements UninformedSearchGateway {
  private readonly httpClient: IHttpClient;
  private readonly baseUrl = '/search/uninformed';

  constructor(httpClient: IHttpClient) {
    this.httpClient = httpClient;
  }

  async breadthFirst(payload: BaseInput): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/breadth_first`,
    });
    return response.data;
  }

  async depthFirst(payload: BaseInput): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/depth_first`,
    });
    return response.data;
  }

  async depthLimited(payload: DepthLimited): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/depth_limited`,
    });
    return response.data;
  }

  async iterativeDeepening(payload: IterativeDeepening): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/iterative_deepening`,
    });
    return response.data;
  }

  async bidirectional(payload: BaseInput): BaseOutput {
    const response = await this.httpClient.post<BaseOutput>({
      payload,
      url: `${this.baseUrl}/bidirectional`,
    });
    return response.data;
  }
}
