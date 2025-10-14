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
}
