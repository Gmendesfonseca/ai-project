import { useForm } from 'react-hook-form';
import { methodOptions, SearchTypes } from '../utils/constants';
import { AxiosHttpAdapter } from '@core/infra/http/axios.adapter';
import { UninformedSearchHttpGateway } from '@core/infra/gateways/http/uninformed-search.gateway';
import { InformedSearchHttpGateway } from '@core/infra/gateways/http/informed-search.gateway';
import { parseFileContent } from '../utils/parseFileContent';
import { parseGraph } from '../utils/parseGraph';
import type { Graph } from '..';
import Select from '@/components/Select';
import Label from '@/components/Label';
import HelperText from '@/components/HelperText';
import Input from '@/components/Input';
import FileInput from '@/components/FileInput';

interface SearchFormData {
  type: SearchTypes;
  start: string;
  goal: string;
  limit: number;
  maxLimit: number;
}

const defaultValues: SearchFormData = {
  type: SearchTypes.BREADTH,
  start: '',
  goal: '',
  limit: 0,
  maxLimit: 0,
};

type Props = {
  setGraph: React.Dispatch<React.SetStateAction<Graph>>;
  graph: Graph;
  setResponse: React.Dispatch<React.SetStateAction<string[] | null>>;
  setError: React.Dispatch<React.SetStateAction<string | null>>;
  startTransition: (callback: () => void) => void;
  loading: boolean;
};

export default function Form({
  setGraph,
  graph,
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
    reset,
  } = useForm<SearchFormData>({
    defaultValues,
  });

  const watchType = watch('type');

  const httpClient = new AxiosHttpAdapter();
  const gateway = {
    uniformed: new UninformedSearchHttpGateway(httpClient),
    informed: new InformedSearchHttpGateway(httpClient),
  };

  async function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    const lines = text.split('\n').map((line) => line.trim());
    lines.pop();
    const graph = parseFileContent(lines);
    setGraph(graph);
    reset({
      type: SearchTypes.BREADTH,
      start: graph.nodes[0] || '',
      goal: graph.nodes[1] || '',
      limit: 0,
      maxLimit: 0,
    });
    event.target.value = '';
  }

  async function onSubmit(data: SearchFormData) {
    startTransition(async () => {
      setError(null);

      try {
        if (!graph.nodes.includes(data.start)) {
          throw new Error(
            `O nó inicial '${data.start}' não existe nos nós fornecidos.`,
          );
        }
        if (!graph.nodes.includes(data.goal)) {
          throw new Error(
            `O nó objetivo '${data.goal}' não existe nos nós fornecidos.`,
          );
        }

        const baseParams = {
          start: data.start,
          goal: data.goal,
          nodes: graph.nodes,
          graph: parseGraph(graph),
        };

        const options = {
          [SearchTypes.BREADTH]: () =>
            gateway.uniformed.breadthFirst(baseParams),
          [SearchTypes.DEPTH]: () => gateway.uniformed.depthFirst(baseParams),
          [SearchTypes.DEPTH_LIMITED]: () =>
            gateway.uniformed.depthLimited({
              ...baseParams,
              limit: Number(data.limit),
            }),
          [SearchTypes.ITERATIVE]: () =>
            gateway.uniformed.iterativeDeepening({
              ...baseParams,
              max_limit: Number(data.maxLimit),
            }),
          [SearchTypes.BIDIRECTIONAL]: () =>
            gateway.uniformed.bidirectional(baseParams),
          [SearchTypes.UNIFORMED_COST]: () =>
            gateway.informed.uniformCost({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
          [SearchTypes.A_STAR]: () =>
            gateway.informed.aStar({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
          [SearchTypes.GREEDY]: () =>
            gateway.informed.greedy({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
          [SearchTypes.IDA_STAR]: () =>
            gateway.informed.idaStar({
              ...baseParams,
              heuristics: graph.nodes.map(() => 0),
            }),
        };

        const response = await options[data.type]();
        setResponse(response?.path || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Ocorreu um erro');
        setResponse(null);
      }
    });
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} style={{ marginBottom: '30px' }}>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '20px',
        }}
      >
        <div>
          <FileInput
            handleFileUpload={handleFileUpload}
            helper={
              <div
                style={{ marginTop: '8px', color: '#666', fontSize: '13px' }}
              >
                {graph.nodes.length > 0 ? (
                  <span>
                    Arquivo carregado: <strong>{graph.nodes.length} nós</strong>
                  </span>
                ) : (
                  <span>Nenhum arquivo carregado</span>
                )}
              </div>
            }
          />
        </div>
        <div>
          <Label>Algoritmo de Busca:</Label>
          <Select
            options={methodOptions}
            disabled={graph.nodes.length === 0}
            {...register('type')}
            style={{
              width: '300px',
              padding: '8px',
              marginBottom: '10px',
              boxSizing: 'border-box',
            }}
          />
        </div>

        <div>
          <Label>Nó Inicial:</Label>
          <Select
            options={graph.nodes.map((node) => ({ label: node, value: node }))}
            {...register('start', {
              required: 'O nó inicial é obrigatório',
              validate: (value) =>
                value !== watch('goal') ||
                'O nó inicial não pode ser o mesmo que o nó objetivo',
            })}
          />
          {errors.start && <HelperText>{errors.start.message}</HelperText>}
        </div>

        <div>
          <Label>Nó Objetivo:</Label>
          <Select
            options={graph.nodes.map((node) => ({ label: node, value: node }))}
            {...register('goal', {
              required: 'O nó objetivo é obrigatório',
              validate: (value) =>
                value !== watch('start') ||
                'O nó objetivo não pode ser o mesmo que o nó inicial',
            })}
          />
          {errors.goal && <HelperText>{errors.goal.message}</HelperText>}
        </div>

        {watchType === SearchTypes.DEPTH_LIMITED && (
          <Input
            min="1"
            type="number"
            placeholder="3"
            label="Limite de Profundidade:"
            error={errors.limit?.message}
            {...register('limit', {
              required:
                'O limite é obrigatório para busca limitada em profundidade',
            })}
          />
        )}

        {watchType === SearchTypes.ITERATIVE && (
          <Input
            min="1"
            type="number"
            placeholder="5"
            error={errors.maxLimit?.message}
            label="Limite Máximo de Profundidade:"
            {...register('maxLimit', {
              required:
                'O limite máximo é obrigatório para busca em profundidade iterativa',
            })}
          />
        )}
      </div>

      <button
        type="submit"
        disabled={loading}
        style={{
          padding: '12px 24px',
          backgroundColor: loading ? '#ccc' : '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer',
          fontSize: '16px',
          marginTop: '20px',
        }}
      >
        {loading ? 'Buscando...' : 'Executar Busca'}
      </button>
    </form>
  );
}
