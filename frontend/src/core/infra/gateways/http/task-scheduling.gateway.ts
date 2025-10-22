import type { IHttpClient } from '@core/domain/ports/http-client.port';
import type {
  TaskSchedulingGateway,
  TaskSchedulingInput,
  TaskSchedulingOutput,
} from '@core/domain/gateway/task-scheduling.gateway';

export class TaskSchedulingHttpGateway implements TaskSchedulingGateway {
  private readonly httpClient: IHttpClient;
  private readonly baseUrl = '/scheduling/task-sequence';

  constructor(httpClient: IHttpClient) {
    this.httpClient = httpClient;
  }

  async aStar(payload: TaskSchedulingInput): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/a_star`,
    });
    return response.data;
  }

  async greedy(payload: TaskSchedulingInput): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/greedy`,
    });
    return response.data;
  }

  async uniformCost(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/uniform_cost`,
    });
    return response.data;
  }

  async breadthFirst(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/breadth_first`,
    });
    return response.data;
  }

  async depthFirst(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/depth_first`,
    });
    return response.data;
  }

  async depthLimited(payload: TaskSchedulingInput): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/depth_limited`,
    });
    return response.data;
  }

  async iterativeDeepening(payload: TaskSchedulingInput): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/iterative_deepening`,
    });
    return response.data;
  }

  async bidirectional(
    payload: Omit<TaskSchedulingInput, 'heuristic' | 'families'>,
  ): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/bidirectional`,
    });
    return response.data;
  }

  async idaStar(payload: TaskSchedulingInput): TaskSchedulingOutput {
    const response = await this.httpClient.post<TaskSchedulingOutput>({
      payload,
      url: `${this.baseUrl}/ida_star`,
    });
    return response.data;
  }
}
