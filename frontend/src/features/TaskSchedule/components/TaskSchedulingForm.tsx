import { useForm } from 'react-hook-form';
import {
  taskSchedulingOptions,
  TaskSchedulingTypes,
  heuristicOptions,
} from '../../Methods/utils/constants';
import { AxiosHttpAdapter } from '@core/infra/http/axios.adapter';
import { TaskSchedulingHttpGateway } from '@core/infra/gateways/http/task-scheduling.gateway';
import type { TaskSchedulingData } from '..';
import type { TaskSchedulingResponse } from '@core/domain/gateway/task-scheduling.gateway';
import Select from '@/components/Select';
import Label from '@/components/Label';
import HelperText from '@/components/HelperText';
import Input from '@/components/Input';

interface TaskSchedulingFormData {
  type: TaskSchedulingTypes;
  tasks: string;
  setupMatrix: string;
  heuristic: string;
  families?: string;
}

const defaultValues: TaskSchedulingFormData = {
  type: TaskSchedulingTypes.TASK_A_STAR,
  tasks: '',
  setupMatrix: '',
  heuristic: 'h1',
  families: '',
};

type Props = {
  setData: React.Dispatch<React.SetStateAction<TaskSchedulingData>>;
  setResponse: React.Dispatch<
    React.SetStateAction<TaskSchedulingResponse | null>
  >;
  setError: React.Dispatch<React.SetStateAction<string | null>>;
  startTransition: (callback: () => void) => void;
  loading: boolean;
};

export default function TaskSchedulingForm({
  setData,
  setResponse,
  setError,
  startTransition,
  loading,
}: Props) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    setValue,
  } = useForm<TaskSchedulingFormData>({
    defaultValues,
  });

  const watchType = watch('type');

  const httpClient = new AxiosHttpAdapter();
  const gateway = new TaskSchedulingHttpGateway(httpClient);

  function parseSetupMatrix(matrixStr: string): Record<string, number> {
    try {
      const lines = matrixStr.trim().split('\n');
      const setupMatrix: Record<string, number> = {};

      for (const line of lines) {
        const match = line.match(/\((\d+),(\d+)\):\s*(\d+(?:\.\d+)?)/);
        if (match) {
          const [, from, to, cost] = match;
          setupMatrix[`(${from},${to})`] = parseFloat(cost);
        }
      }

      return setupMatrix;
    } catch (error) {
      throw new Error(
        'Formato inválido para matriz de setup. Use: (origem,destino): custo',
      );
    }
  }

  function parseFamilies(
    familiesStr: string,
  ): Record<number, string> | undefined {
    if (!familiesStr.trim()) return undefined;

    try {
      const lines = familiesStr.trim().split('\n');
      const families: Record<number, string> = {};

      for (const line of lines) {
        const match = line.match(/(\d+):\s*(.+)/);
        if (match) {
          const [, task, family] = match;
          families[parseInt(task)] = family.trim();
        }
      }

      return Object.keys(families).length > 0 ? families : undefined;
    } catch (error) {
      throw new Error('Formato inválido para famílias. Use: tarefa: família');
    }
  }

  async function onSubmit(formData: TaskSchedulingFormData) {
    startTransition(async () => {
      setError(null);
      setResponse(null);

      try {
        // Parse tasks
        const tasks = formData.tasks
          .split(',')
          .map((t) => parseInt(t.trim()))
          .filter((t) => !isNaN(t));

        if (tasks.length === 0) {
          throw new Error('Adicione pelo menos uma tarefa');
        }

        // Parse setup matrix
        const setupMatrix = parseSetupMatrix(formData.setupMatrix);

        // Parse families (optional)
        const families = formData.families
          ? parseFamilies(formData.families)
          : undefined;

        // Update local state
        const taskData: TaskSchedulingData = {
          tasks,
          setupMatrix,
          families,
        };
        setData(taskData);

        // Prepare request payload
        const payload = {
          tasks,
          setup_matrix: setupMatrix,
          heuristic: formData.heuristic,
          families,
        };

        let result: TaskSchedulingResponse | null = null;

        // Call appropriate algorithm
        switch (formData.type) {
          case TaskSchedulingTypes.TASK_A_STAR:
            result = await gateway.aStar(payload);
            break;
          case TaskSchedulingTypes.TASK_GREEDY:
            result = await gateway.greedy(payload);
            break;
          case TaskSchedulingTypes.TASK_UNIFORM_COST:
            result = await gateway.uniformCost({
              tasks: payload.tasks,
              setup_matrix: payload.setup_matrix,
            });
            break;
          default:
            throw new Error('Algoritmo não implementado');
        }

        if (result) {
          setResponse(result);
        } else {
          throw new Error('Nenhuma solução encontrada');
        }
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : 'Erro desconhecido ao executar algoritmo',
        );
      }
    });
  }

  // Load example data
  function loadExample() {
    setValue('tasks', '1,2,3,4');
    setValue(
      'setupMatrix',
      `(0,1): 10
(0,2): 15
(0,3): 20
(0,4): 25
(1,2): 5
(1,3): 10
(1,4): 15
(2,1): 8
(2,3): 6
(2,4): 12
(3,1): 12
(3,2): 7
(3,4): 4
(4,1): 18
(4,2): 14
(4,3): 6`,
    );
    setValue(
      'families',
      `1: ProductA
2: ProductA
3: ProductB
4: ProductB`,
    );
  }

  return (
    <div
      style={{
        width: '300px',
        minWidth: '300px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
      }}
    >
      <form onSubmit={handleSubmit(onSubmit)}>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '15px',
          }}
        >
          <div>
            <Label>Algoritmo</Label>
            <Select
              id="type"
              {...register('type', { required: true })}
              options={taskSchedulingOptions}
            />
            {errors.type && <HelperText>Campo obrigatório</HelperText>}
          </div>

          {(watchType === TaskSchedulingTypes.TASK_A_STAR ||
            watchType === TaskSchedulingTypes.TASK_GREEDY) && (
            <div>
              <Label>Heurística</Label>
              <Select
                id="heuristic"
                {...register('heuristic')}
                options={heuristicOptions}
              />
            </div>
          )}

          <div>
            <Label>Tarefas (separadas por vírgula)</Label>
            <Input
              id="tasks"
              placeholder="1,2,3,4"
              {...register('tasks', { required: true })}
            />
            {errors.tasks && <HelperText>Campo obrigatório</HelperText>}
          </div>

          <div>
            <Label>Matriz de Setup</Label>
            <textarea
              id="setupMatrix"
              placeholder="(0,1): 10&#10;(0,2): 15&#10;..."
              {...register('setupMatrix', { required: true })}
              style={{
                width: '100%',
                minHeight: '120px',
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '12px',
              }}
            />
            {errors.setupMatrix && <HelperText>Campo obrigatório</HelperText>}
          </div>

          {(watchType === TaskSchedulingTypes.TASK_A_STAR ||
            watchType === TaskSchedulingTypes.TASK_GREEDY) &&
            watch('heuristic') === 'h3' && (
              <div>
                <Label>Famílias de Produtos (opcional)</Label>
                <textarea
                  id="families"
                  placeholder="1: ProductA&#10;2: ProductA&#10;3: ProductB"
                  {...register('families')}
                  style={{
                    width: '100%',
                    minHeight: '80px',
                    padding: '8px',
                    border: '1px solid #ccc',
                    borderRadius: '4px',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                  }}
                />
              </div>
            )}

          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              type="submit"
              disabled={loading}
              style={{
                flex: 1,
                padding: '10px',
                backgroundColor: loading ? '#ccc' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? 'Executando...' : 'Executar'}
            </button>

            <button
              type="button"
              onClick={loadExample}
              style={{
                padding: '10px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Exemplo
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
