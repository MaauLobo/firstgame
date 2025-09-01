# 🏎️ GAME DESIGN DOCUMENT (GDD)
# VELOZES E ASSADOS

---

## 📋 **INFORMAÇÕES BÁSICAS**

- **Título**: Velozes e Assados
- **Gênero**: Corrida / Arcade / Endless Runner
- **Plataforma**: PC (Windows, Linux, macOS)
- **Motor**: Pygame
- **Resolução**: 1280x720 (16:9)
- **FPS**: 60 FPS
- **Idioma**: Português
- **Classificação Indicativa**: Livre para todas as idades

---

## 🎯 **CONCEITO DO JOGO**

### **Visão Geral**
"Velozes e Assados" é um jogo de corrida em terceira pessoa onde o jogador controla um carro em uma estrada infinita, desviando de obstáculos e tentando sobreviver o máximo tempo possível. O jogo combina elementos de arcade clássico com mecânicas modernas como sistema de playlist dinâmica e IA inteligente para carros da polícia.

### **Objetivo Principal**
Sobreviver o máximo tempo possível na estrada, desviando de obstáculos e acumulando pontos. O jogo não tem fim definido - é um desafio contínuo de habilidade e reflexos.

### **Público-Alvo**
- **Idade**: 8+ anos
- **Interesse**: Jogos de corrida, arcade, desafios de habilidade
- **Experiência**: Iniciantes a jogadores experientes

---

## 🎮 **MECÂNICAS DE JOGO**

### **Controles Principais**
- **Setas Esquerda/Direita** ou **A/D**: Movimento lateral do carro
- **ESPAÇO**: Iniciar jogo (menu)
- **R**: Reiniciar após game over

### **Controles da Playlist (Durante o Jogo)**
- **N**: Próxima música
- **R**: Música aleatória
- **P**: Pausar/Despausar música
- **M**: Mudo/Desmudo

### **Mecânicas Core**
1. **Movimento Lateral**: Carro se move apenas horizontalmente em 3 faixas
2. **Velocidade Progressiva**: A estrada acelera gradualmente
3. **Sistema de Pontuação**: 1 ponto por obstáculo evitado
4. **Dificuldade Escalável**: Aumenta a cada 10 pontos
5. **Spawn Dinâmico**: Obstáculos aparecem mais rapidamente conforme a dificuldade

---

## 🚗 **ENTIDADES DO JOGO**

### **Carro do Jogador**
- **Velocidade**: 380 px/s
- **Altura**: 90px (escalável)
- **Movimento**: Apenas lateral (esquerda/direita)
- **Colisão**: Sistema de máscara com threshold de opacidade
- **Posicionamento**: Inicia na faixa central

### **Obstáculos**
- **Tipos**: Taxi, Audi, Car, Police
- **Altura**: 90px (escalável)
- **Velocidade Inicial**: 280 px/s
- **Spawn**: A cada 0.7 segundos (diminui com dificuldade)
- **Comportamento**: Movimento vertical descendente

### **Carro da Polícia (Especial)**
- **Chance de Spawn**: 15%
- **Características Únicas**:
  - Sirene animada (3 frames)
  - Movimento lateral inteligente
  - Tenta bloquear o jogador
  - Efeitos visuais especiais
- **IA**: Detecta posição do jogador e tenta interceptar
- **Movimento Lateral**: 120 px/s
- **Intervalo de Mudança de Faixa**: 1.5s (diminui com dificuldade)

---

## 🎵 **SISTEMA DE ÁUDIO**

### **Música de Abertura**
- **Arquivo**: `abertura.mp3`
- **Reprodução**: Loop infinito no menu
- **Transição**: Para automaticamente ao iniciar o jogo

### **Playlist do Jogo**
- **Localização**: `assets/sounds/playlist/`
- **Formatos Suportados**: MP3, WAV, OGG
- **Volume Padrão**: 70%
- **Modo Agressivo**: Volume aumenta com dificuldade
- **Fade Time**: 1 segundo entre transições
- **Reprodução**: Aleatória com controles manuais

### **Controles da Playlist**
- **Automático**: Música muda automaticamente ao terminar
- **Manual**: Controles para próxima, aleatória, pausar, mudo
- **Transições Suaves**: Fade in/out entre músicas

---

## 🖥️ **INTERFACE DO USUÁRIO**

### **Tela de Abertura**
- **Imagem**: `abertura.png`
- **Instruções**: "Pressione ESPAÇO para jogar"
- **Música**: Trilha de abertura em loop

### **HUD Durante o Jogo**
- **Pontuação**: Canto superior esquerdo
- **Aviso de Polícia**: "🚨 CARRO DA POLÍCIA! 🚨" (vermelho)
- **Informações da Música**: Nome da música atual
- **Controles da Playlist**: Dicas de teclas

### **Tela de Game Over**
- **Imagem**: `gameover.png`
- **Pontuação Final**: Exibida centralmente
- **Instruções**: "Pressione R para jogar novamente"

---

## 🛣️ **AMBIENTE E VISUAIS**

### **Estrada**
- **Imagem**: `road.png`
- **Largura**: 40% da tela
- **Posicionamento**: Centralizada
- **Movimento**: Scroll infinito vertical
- **Aceleração**: 8 px/s²
- **Faixas**: 3 faixas detectadas automaticamente

### **Detecção de Asfalto**
- **Sistema**: Análise automática de pixels
- **Threshold**: 50 de opacidade
- **Faixas**: Calculadas dinamicamente
- **Margens**: 6px de folga lateral

### **Efeitos Visuais**
- **Sirene da Polícia**: Animação de 3 frames
- **Efeito de Brilho**: Luz vermelha piscante
- **Raio de Luz**: Efeito circular da sirene
- **Setas de Movimento**: Indicam direção da polícia

---

## 💥 **SISTEMA DE COLISÃO**

### **Modos de Colisão**
- **Padrão**: Sistema de máscara (mask)
- **Alternativo**: Sistema de redução de hitbox (shrink)
- **Threshold**: 50 de opacidade para transparência

### **Hitbox do Jogador**
- **Tipo**: Retângulo com máscara de transparência
- **Debug**: Opcional (SHOW_HITBOX_DEBUG)

### **Hitbox dos Obstáculos**
- **Tipo**: Retângulo com máscara de transparência
- **Cores Debug**: Verde (jogador), Vermelho (obstáculos)

---

## 📊 **SISTEMA DE PROGRESSÃO**

### **Dificuldade**
- **Inicial**: Nível 1
- **Aumento**: A cada 10 pontos
- **Efeitos**:
  - Velocidade dos obstáculos +40 px/s
  - Intervalo de spawn reduzido
  - Volume da playlist aumenta
  - Polícia fica mais agressiva

### **Pontuação**
- **Sistema**: 1 ponto por obstáculo evitado
- **Persistência**: Mantida até colisão
- **Display**: Atualizada em tempo real

### **Velocidade da Estrada**
- **Inicial**: 200 px/s
- **Aceleração**: 8 px/s²
- **Máxima**: Sem limite (aumenta continuamente)

---

## 🔧 **ARQUITETURA TÉCNICA**

### **Estrutura Modular**
```
src/
├── config.py          # Configurações e constantes
├── game_states.py     # Gerenciamento de estados
├── entities/          # Entidades do jogo
├── managers/          # Gerenciadores de sistemas
├── utils/             # Utilitários
└── ui/                # Interface do usuário
```

### **Estados do Jogo**
1. **MENU (0)**: Tela de abertura
2. **JOGANDO (1)**: Gameplay ativo
3. **GAME_OVER (2)**: Tela de fim de jogo

### **Gerenciadores**
- **GameStateManager**: Controla transições de estado
- **PlaylistManager**: Gerencia reprodução de música
- **CollisionManager**: Sistema de detecção de colisões

---

## 🎨 **ASSETS E RECURSOS**

### **Imagens**
- **Carros**: `carro_jogador.png`, `taxi.png`, `audi.png`, `car.png`
- **Polícia**: `police.png` + animação (3 frames)
- **Ambiente**: `road.png`, `road.svg`
- **UI**: `abertura.png`, `gameover.png`

### **Sons**
- **Menu**: `abertura.mp3`
- **Playlist**: Músicas na pasta `playlist/`

### **Especificações Técnicas**
- **Formato de Imagem**: PNG com transparência
- **Formato de Áudio**: MP3, WAV, OGG
- **Otimização**: Conversão para alpha e máscaras

---

## 🚀 **FUNCIONALIDADES FUTURAS**

### **Curto Prazo**
- [ ] Sistema de power-ups
- [ ] Múltiplos tipos de estrada
- [ ] Efeitos sonoros adicionais
- [ ] Sistema de conquistas

### **Médio Prazo**
- [ ] Modo multiplayer local
- [ ] Diferentes carros para o jogador
- [ ] Sistema de níveis
- [ ] Modo história

### **Longo Prazo**
- [ ] Modo online
- [ ] Editor de níveis
- [ ] Sistema de ranking
- [ ] Modo torneio

---

## 🧪 **TESTES E QUALIDADE**

### **Testes de Funcionalidade**
- [x] Sistema de colisão
- [x] Movimento do jogador
- [x] Spawn de obstáculos
- [x] Sistema de pontuação
- [x] Playlist de música
- [x] IA da polícia

### **Testes de Performance**
- [x] 60 FPS estável
- [x] Detecção de colisão otimizada
- [x] Gerenciamento de memória
- [x] Transições suaves

### **Testes de Usabilidade**
- [x] Controles responsivos
- [x] Interface clara
- [x] Feedback visual
- [x] Instruções claras

---

## 📝 **INSTRUÇÕES DE INSTALAÇÃO**

### **Requisitos do Sistema**
- **Python**: 3.7+
- **Pygame**: 2.0+
- **Sistema Operacional**: Windows, Linux, macOS

### **Instalação**
```bash
# Clonar repositório
git clone [URL_DO_REPOSITORIO]
cd firstgame

# Instalar dependências
pip install pygame

# Executar jogo
python main_new.py
```

### **Estrutura de Arquivos**
```
firstgame/
├── main_new.py        # Arquivo principal
├── src/               # Código fonte
├── assets/            # Recursos
└── README.md          # Documentação
```

---

## 🎯 **OBJETIVOS DE DESIGN**

### **Principais**
1. **Acessibilidade**: Fácil de aprender, difícil de dominar
2. **Replayability**: Jogabilidade infinita e viciante
3. **Feedback**: Resposta imediata às ações do jogador
4. **Progressão**: Sensação de evolução constante

### **Secundários**
1. **Imersão**: Sistema de áudio dinâmico
2. **Desafio**: IA inteligente para carros da polícia
3. **Personalização**: Controles da playlist
4. **Polimento**: Efeitos visuais e transições suaves

---

## 📊 **MÉTRICAS DE SUCESSO**

### **Quantitativas**
- **Tempo de Jogo**: Média de 5+ minutos por sessão
- **Retenção**: 70% dos jogadores retornam após primeira sessão
- **Pontuação**: Média de 50+ pontos por jogador
- **Performance**: 60 FPS estável em 95% dos casos

### **Qualitativas**
- **Feedback do Usuário**: Avaliação 4.5+/5
- **Facilidade de Uso**: Aprendizado em menos de 2 minutos
- **Satisfação**: Jogadores querem jogar novamente
- **Recomendação**: 80% recomendariam para amigos

---

## 🔮 **ROADMAP DE DESENVOLVIMENTO**

### **Fase 1 (Atual)**
- [x] Arquitetura modular implementada
- [x] Sistema de playlist funcional
- [x] IA da polícia implementada
- [x] Sistema de colisão otimizado

### **Fase 2 (Próximas 2-4 semanas)**
- [ ] Sistema de power-ups básico
- [ ] Novos tipos de obstáculos
- [ ] Efeitos sonoros adicionais
- [ ] Sistema de conquistas simples

### **Fase 3 (Próximos 2-3 meses)**
- [ ] Modo multiplayer local
- [ ] Sistema de níveis
- [ ] Diferentes carros para o jogador
- [ ] Modo história básico

### **Fase 4 (Próximos 6 meses)**
- [ ] Modo online
- [ ] Editor de níveis
- [ ] Sistema de ranking
- [ ] Modo torneio

---

## 📞 **CONTATO E SUPORTE**

### **Desenvolvedor**
- **Nome**: [NOME_DO_DESENVOLVEDOR]
- **Email**: [EMAIL]
- **GitHub**: [LINK_DO_GITHUB]

### **Documentação**
- **Arquitetura**: `ARQUITETURA.md`
- **README**: `README.md`
- **GDD**: Este documento

### **Repositório**
- **URL**: [LINK_DO_REPOSITORIO]
- **Licença**: [TIPO_DE_LICENÇA]
- **Versão**: 1.0.0

---

## 📋 **CHECKLIST DE IMPLEMENTAÇÃO**

### **Core Gameplay**
- [x] Movimento do jogador
- [x] Sistema de obstáculos
- [x] Colisões
- [x] Pontuação
- [x] Dificuldade progressiva

### **Sistemas**
- [x] Estados do jogo
- [x] Sistema de áudio
- [x] Playlist dinâmica
- [x] IA da polícia
- [x] Interface do usuário

### **Qualidade**
- [x] Arquitetura modular
- [x] Código limpo e documentado
- [x] Performance otimizada
- [x] Tratamento de erros
- [x] Sistema de debug

---

**🎉 Este GDD representa a documentação completa do jogo "Velozes e Assados" e deve ser atualizado conforme o desenvolvimento avança.**

**📅 Última Atualização**: [DATA]
**📝 Versão do Documento**: 1.0
**👨‍💻 Preparado por**: [NOME_DO_DESENVOLVEDOR] 