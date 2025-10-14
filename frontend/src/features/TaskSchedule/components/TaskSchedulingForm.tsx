import { useForm } from 'react-hook-form';
import {
  taskSchedulingOptions,
  TaskSchedulingTypes,
  heuristicOptions,
} from '../../Methods/utils/constants';
import { AxiosHttpAdapter } from '@core/infra/http/axios.adapter';
import { TaskSchedulingHttpGateway } from '@core/infra/gateways/http/task-scheduling.gateway';
import { parseTaskFile } from '../utils/parseTaskFile';
import {
  formatTaskDataForDisplay,
  validateTaskData,
} from '../utils/formatTaskData';
import { TASK_FILE_EXAMPLE } from '../utils/constants';
import type { TaskSchedulingData } from '..';
import type { TaskSchedulingResponse } from '@core/domain/gateway/task-scheduling.gateway';
import Select from '@/components/Select';
import Label from '@/components/Label';
import HelperText from '@/components/HelperText';
import Input from '@/components/Input';
import FileInput from '@/components/FileInput';

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
  data: TaskSchedulingData;
  setData: React.Dispatch<React.SetStateAction<TaskSchedulingData>>;
  setResponse: React.Dispatch<
    React.SetStateAction<TaskSchedulingResponse | null>
  >;
  setError: React.Dispatch<React.SetStateAction<string | null>>;
  startTransition: (callback: () => void) => void;
  loading: boolean;
};

export default function TaskSchedulingForm({
  data,
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

  async function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const text = await file.text();
      const lines = text.split('\n').map((line) => line.trim());
      const parsedData = parseTaskFile(lines);

      // Validate the parsed data
      const validationErrors = validateTaskData(parsedData);
      if (validationErrors.length > 0) {
        setError(`Erro no arquivo: ${validationErrors.join(', ')}`);
        return;
      }

      // Update data state (without families from file)
      const dataWithoutFamilies = { ...parsedData, families: undefined };
      setData(dataWithoutFamilies);

      // Format data for form display
      const { tasksString, setupMatrixString } =
        formatTaskDataForDisplay(parsedData);

      // Update form values (don't override families - keep user input)
      setValue('tasks', tasksString);
      setValue('setupMatrix', setupMatrixString);

      // Clear any previous errors
      setError(null);

      // Clear the file input
      event.target.value = '';
    } catch (error) {
      setError(
        `Erro ao processar arquivo: ${
          error instanceof Error ? error.message : 'Erro desconhecido'
        }`,
      );
    }
  }

  function parseSetupMatrix(matrixStr: string): Record<string, number> {
    try {
      const lines = matrixStr.trim().split('\n');
      const setupMatrix: Record<string, number> = {};

      for (const line of lines) {
        // Support both formats: "(0,1): 10" and "0,1:10"
        const match = line.match(/\(?(\d+),(\d+)\)?:\s*(\d+(?:\.\d+)?)/);
        if (match) {
          const [, from, to, cost] = match;
          setupMatrix[`(${from},${to})`] = parseFloat(cost);
        }
      }

      return setupMatrix;
    } catch (error) {
      throw new Error(
        'Formato inválido para matriz de setup. Use: origem,destino:custo',
      );
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

        // Parse families from individual task inputs (optional)
        const families: Record<number, string> = {};
        let hasFamilies = false;

        // Collect family data from individual task inputs
        for (const task of tasks) {
          const familyValue = (formData as any)[`family_${task}`];
          if (familyValue && familyValue.trim()) {
            families[task] = familyValue.trim();
            hasFamilies = true;
          }
        }

        const finalFamilies = hasFamilies ? families : undefined;

        // Update local state
        const taskData: TaskSchedulingData = {
          tasks,
          setupMatrix,
          families: finalFamilies,
        };
        setData(taskData);

        // Prepare request payload
        const payload = {
          tasks,
          setup_matrix: setupMatrix,
          heuristic: formData.heuristic,
          families: finalFamilies,
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
      `0,1:25
0,2:15
0,3:20
0,4:10
1,2:5
1,3:10
1,4:15
2,1:8
2,3:6
2,4:12
3,1:12
3,2:7
3,4:4
4,1:18
4,2:14
4,3:6`,
    );
    setValue(
      'families',
      `1: ProductA
2: ProductA
3: ProductB
4: ProductB`,
    );
  }

  // Download example file
  function downloadExampleFile() {
    const blob = new Blob([TASK_FILE_EXAMPLE], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'task_scheduling_example.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
            <FileInput
              handleFileUpload={handleFileUpload}
              helper={
                <div
                  style={{ marginTop: '8px', color: '#666', fontSize: '13px' }}
                >
                  {data.tasks.length > 0 ? (
                    <span>
                      Arquivo carregado:{' '}
                      <strong>{data.tasks.length} tarefas</strong> (
                      {data.tasks.join(', ')})
                    </span>
                  ) : (
                    <span>Formato: origem,destino:custo (ex: 0,1:25)</span>
                  )}
                </div>
              }
            />
          </div>

          <div>
            <Label>Algoritmo</Label>
            <Select
              id="type"
              {...register('type', { required: true })}
              options={taskSchedulingOptions}
              disabled={data.tasks.length === 0}
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
              disabled
              {...register('tasks', { required: true })}
            />
            {errors.tasks && <HelperText>Campo obrigatório</HelperText>}
          </div>

          <div>
            <Label>Matriz de Setup</Label>
            <textarea
              id="setupMatrix"
              placeholder="0,1:25&#10;0,2:15&#10;1,2:5&#10;..."
              disabled
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
                {data.tasks.length > 0 ? (
                  <div
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '8px',
                      maxHeight: '200px',
                      overflowY: 'auto',
                      padding: '8px',
                      border: '1px solid #ddd',
                      borderRadius: '4px',
                      backgroundColor: '#f9f9f9',
                    }}
                  >
                    {data.tasks.map((task) => (
                      <div
                        key={task}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px',
                        }}
                      >
                        <label
                          style={{
                            minWidth: '60px',
                            fontSize: '14px',
                            fontWeight: 'bold',
                          }}
                        >
                          Tarefa {task}:
                        </label>
                        <Input
                          placeholder={`Família da tarefa ${task}`}
                          {...register(`family_${task}` as any)}
                          style={{
                            flex: 1,
                            padding: '4px 8px',
                            fontSize: '12px',
                          }}
                        />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div
                    style={{
                      padding: '12px',
                      textAlign: 'center',
                      color: '#666',
                      fontStyle: 'italic',
                      border: '1px dashed #ccc',
                      borderRadius: '4px',
                    }}
                  >
                    Carregue um arquivo para definir famílias das tarefas
                  </div>
                )}
              </div>
            )}

          <div
            style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}
          >
            <button
              type="submit"
              disabled={loading || data.tasks.length === 0}
              style={{
                padding: '10px',
                backgroundColor:
                  loading || data.tasks.length === 0 ? '#ccc' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor:
                  loading || data.tasks.length === 0
                    ? 'not-allowed'
                    : 'pointer',
              }}
            >
              {loading ? 'Executando...' : 'Executar'}
            </button>

            <div style={{ display: 'flex', gap: '5px' }}>
              <button
                type="button"
                onClick={loadExample}
                style={{
                  flex: 1,
                  padding: '8px',
                  backgroundColor: '#28a745',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '12px',
                }}
              >
                Exemplo
              </button>

              <button
                type="button"
                onClick={downloadExampleFile}
                style={{
                  flex: 1,
                  padding: '8px',
                  backgroundColor: '#6c757d',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '12px',
                }}
              >
                ↓ Arquivo
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
