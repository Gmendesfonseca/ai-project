from collections import deque
from Node import Node

class UninformedSearch(object):
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRAFO
    #--------------------------------------------------------------------------
    def sucessores_grafo(self,ind,grafo,ordem):
        
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRID
    #--------------------------------------------------------------------------
    # SUCESSORES PARA GRID (LISTA DE ADJACENCIAS)
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        # DIREITA
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                f.append(suc)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                f.append(suc)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                f.append(suc)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                f.append(suc)
        
        return f
    #--------------------------------------------------------------------------    
    # EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
    #--------------------------------------------------------------------------    
    def exibir_caminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
    #--------------------------------------------------------------------------    
    # CONTROLE DE NÓS REPETIDOS
    #--------------------------------------------------------------------------
    def exibir_caminho1(self,encontro,visitado1, visitado2):
        # nó do lado do início
        encontro1 = visitado1[encontro]  
        # nó do lado do objetivo
        encontro2 = visitado2[encontro]
    
        caminho1 = self.exibir_caminho(encontro1)
        caminho2 = self.exibir_caminho(encontro2)
    
        # Inverte o caminho
        caminho2 = list(reversed(caminho2[:-1]))
    
        return caminho1 + caminho2
    #--------------------------------------------------------------------------
    # BUSCA EM AMPLITUDE
    #--------------------------------------------------------------------------
    #def amplitude(self,start,end,nx,ny,mapa):  # grid
    def amplitude(self,start,end,nodes,grafo):   # grafo
        # Finaliza se início for igual a objetivo
        if start == end:
            return [start]
        
        # GRID: transforma em tupla
        #t_start = tuple(start)   # grid
        #t_end = tuple(end)         # grid
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,start,0,None,None)    # grafo
        #raiz = Node(None,t_start,0,None,None)  # grid
        fila.append(raiz)
    
        # Marca início como visitado
        visitado = {start: raiz}           # grafo
        #visitado = {tuple(start): raiz}    # grid
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.popleft()
    
            # Gera sucessores a partir do grafo
            ind = nodes.index(atual.estado)    # grafo
            filhos = self.sucessores_grafo(ind, grafo, 1) # grafo
            
            # Gera sucessores a partir do grid
            #filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos:
                #t_novo = tuple(novo)       # grid
                #if t_novo not in visitado: # grid
                if novo not in visitado:   # grafo
                    #filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                    filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                    fila.append(filho)
                    visitado[novo] = filho   # grafo
                    #visitado[t_novo] = filho # grid
                    
                    # Verifica se encontrou o objetivo
                    if novo == end:        # grafo
                    #if t_novo == t_end:    # grid
                        return self.exibir_caminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE
    #--------------------------------------------------------------------------
    def profundidade(self, start, end, nodes, grafo):
    #def profundidade(self,start,end,nx,ny,mapa):
        # Finaliza se início for igual a objetivo
        if start == end:
            return [start]
        
        # GRID: transforma em tupla
        #t_start = tuple(start)   # grid
        #t_end = tuple(end)         # grid
        
        # Lista para árvore de busca - FILA
        fila = deque()
    
        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None,start,0,None,None)    # grafo
        #raiz = Node(None,t_start,0,None,None)  # grid
        fila.append(raiz)
    
        # Marca início como visitado
        visitado = {start: raiz}           # grafo
        #visitado = {tuple(start): raiz}    # grid
        
        while fila:
            # Remove o primeiro da FILA
            atual = fila.pop()
    
            # Gera sucessores a partir do grafo
            ind = nodes.index(atual.estado)    # grafo
            filhos = self.sucessores_grafo(ind,grafo,1) # grafo
            
            # Gera sucessores a partir do grid
            #filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos:
                #t_novo = tuple(novo)       # grid
                #if t_novo not in visitado: # grid
                if novo not in visitado:   # grafo
                    #filho = Node(atual,t_novo,atual.v1 + 1,None,None) # grid
                    filho = Node(atual,novo,atual.v1 + 1,None,None)  # grafo
                    fila.append(filho)
                    visitado[novo] = filho   # grafo
                    #visitado[t_novo] = filho # grid
                    
                    # Verifica se encontrou o objetivo
                    if novo == end:        # grafo
                    #if t_novo == t_end:    # grid
                        return self.exibir_caminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM PROFUNDIDADE LIMITADA
    #--------------------------------------------------------------------------
    def prof_limitada(self,start,end,nodes,grafo,lim):
        if start == end:
            return [start]
        
        # Lista para árvore de busca - PILHA
        pilha = deque()
    
        # Inclui início como nó raíz da árvore de busca
        pilha.append(Node(None,start,0,None,None))
    
        # Marca início como visitado
        visitado = {start: 0}
    
        while pilha:
            # Remove o último da PILHA
            atual = pilha.pop()
            
            if atual.v1 < lim:
                # Obtem o índice do estado atual na lista 'nodes'
                ind = nodes.index(atual.estado)
        
                # Gera sucessores a partir do grafo
                filhos = self.sucessores_grafo(ind, grafo,-1)
        
                for novo in filhos:
                    if novo not in visitado:
                        filho = Node(atual,novo,atual.v1 + 1,None,None)
                        pilha.append(filho)
                        visitado[novo] = filho.v1
        
                        # Verifica se encontrou o objetivo
                        if novo == end:
                            return self.exibir_caminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA EM APROFUNDAMENTO ITERATIVO
    #--------------------------------------------------------------------------
    def aprof_iterativo(self,start,end,nodes,grafo,lim_max):
        if start == end:
            return [start]
        
        for lim in range(1,lim_max+1):
            # Lista para árvore de busca - PILHA
            pilha = deque()
        
            # Inclui início como nó raíz da árvore de busca
            pilha.append(Node(None,start,0,None,None))
        
            # Marca início como visitado
            visitado = {start: 0}
        
            while pilha:
                # Remove o último da PILHA
                atual = pilha.pop()
                
                if atual.v1 < lim:
                    # Obtem o índice do estado atual na lista 'nodes'
                    ind = nodes.index(atual.estado)
            
                    # Gera sucessores a partir do grafo
                    filhos = self.sucessores_grafo(ind, grafo,-1)
            
                    for novo in filhos:
                        if novo not in visitado:
                            filho = Node(atual,novo,atual.v1 + 1,None,None)
                            pilha.append(filho)
                            visitado[novo] = filho.v1
            
                            # Verifica se encontrou o objetivo
                            if novo == end:
                                return self.exibir_caminho(filho)
        return None
    #--------------------------------------------------------------------------
    # BUSCA BIDIRECIONAL
    #--------------------------------------------------------------------------
    def bidirecional(self, start, end, nodes, grafo):
        if start == end:
            return [start]

        # Lista para árvore de busca a partir da origem - FILA
        deque1 = deque()
        
        # Lista para árvore de busca a partir do destino - FILA
        deque2 = deque()  
        
        # Inclui início e end como nó raíz da árvore de busca
        deque1.append(Node(None,start,0,None,None))
        deque2.append(Node(None,end,0,None,None))
    
        # Visitados mapeando estado -> Node (para reconstruir o caminho)
        visitado1 = {start: deque1[0]}
        visitado2 = {end:    deque2[0]}
        
        nivel = 0
    
        while deque1 and deque2:
            
            # ****** Executa AMPLITUDE a partir da ORIGEM *******
            # Quantidade de nós no nível atual
            nivel = len(deque1)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = deque1.popleft()

                # Gera sucessores
                ind = nodes.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)

                for novo in filhos:
                    if novo not in visitado1:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado1[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado2:
                            return self.exibir_caminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        deque1.append(filho)
            
            # ****** Executa AMPLITUDE a partir do OBJETIVO *******
            # Quantidade de nós no nível atual
            nivel = len(deque2)  
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = deque2.popleft()

                # Gera sucessores
                ind = nodes.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)

                for novo in filhos:
                    if novo not in visitado2:
                        filho = Node(atual,novo,atual.v1 + 1,None, None)
                        visitado2[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado1:
                            return self.exibir_caminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        deque2.append(filho)
        return None
