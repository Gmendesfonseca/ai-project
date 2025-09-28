import type { IHttpClient } from '../../../domain/ports/http-client.port';
import type {
  BaseUniformedOutput,
  BaseUninformedInput,
  DepthLimited,
  IterativeDeepening,
  UninformedSearchGateway,
} from '../../../domain/gateway/uninformed-search.gateway';

export class UninformedSearchHttpGateway implements UninformedSearchGateway {
  private readonly httpClient: IHttpClient;

  constructor(httpClient: IHttpClient) {
    this.httpClient = httpClient;
  }

  async breadthFirst(payload: BaseUninformedInput): BaseUniformedOutput {
    const response = await this.httpClient.post<BaseUniformedOutput>({
      payload,
      url: '/search/uninformed/breadth-first',
    });
    return response.data;
  }

  async depthFirst(payload: BaseUninformedInput): BaseUniformedOutput {
    const response = await this.httpClient.post<BaseUniformedOutput>({
      payload,
      url: '/search/uninformed/depth-first',
    });
    return response.data;
  }

  async depthLimited(payload: DepthLimited): BaseUniformedOutput {
    const response = await this.httpClient.post<BaseUniformedOutput>({
      payload,
      url: '/search/uninformed/depth-limited',
    });
    return response.data;
  }

  async iterativeDeepening(payload: IterativeDeepening): BaseUniformedOutput {
    const response = await this.httpClient.post<BaseUniformedOutput>({
      payload,
      url: '/search/uninformed/iterative-deepening',
    });
    return response.data;
  }

  async bidirectional(payload: BaseUninformedInput): BaseUniformedOutput {
    const response = await this.httpClient.post<BaseUniformedOutput>({
      payload,
      url: '/search/uninformed/bidirectional',
    });
    return response.data;
  }
}
