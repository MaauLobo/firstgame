# 🎁 Guia dos Power-ups - Velozes e Assados

## 📋 Visão Geral

O sistema de power-ups adiciona elementos estratégicos ao jogo, permitindo que o jogador colete vantagens temporárias durante a corrida. Cada power-up tem efeitos únicos que podem ser combinados para criar estratégias interessantes.

## 🎮 Como Acessar a Ajuda

### Durante o Jogo:
- **Tecla H**: Abre a tela de ajuda dos power-ups
- **Tecla H novamente**: Volta ao jogo

### No Menu Principal:
- **Tecla H**: Abre a tela de ajuda dos power-ups
- **Tecla H novamente**: Volta ao menu

## 🛡️ Tipos de Power-ups

### 1. **Escudo** (Ciano)
- **Símbolo**: Triângulo
- **Duração**: 5 segundos
- **Efeito**: Imunidade total contra colisões
- **Estratégia**: Use quando estiver em uma situação difícil ou para passar por obstáculos impossíveis

### 2. **Turbo** (Amarelo)
- **Símbolo**: Seta para cima
- **Duração**: 3 segundos
- **Efeito**: Aumenta velocidade do jogador em 50%
- **Estratégia**: Útil para escapar de situações perigosas ou alcançar power-ups distantes

### 3. **Câmera Lenta** (Roxo)
- **Símbolo**: Relógio
- **Duração**: 4 segundos
- **Efeito**: Reduz velocidade dos obstáculos em 50%
- **Estratégia**: Facilita a navegação em velocidades altas ou quando há muitos obstáculos

### 4. **Ímã** (Magenta)
- **Símbolo**: Formato de U
- **Duração**: 6 segundos
- **Efeito**: Atrai power-ups próximos (raio de 150px)
- **Estratégia**: Colete mais power-ups automaticamente sem precisar se mover muito

### 5. **Pontos Duplos** (Verde)
- **Símbolo**: Dois círculos
- **Duração**: 8 segundos
- **Efeito**: Duplica a pontuação ganha
- **Estratégia**: Use quando estiver confiante para maximizar a pontuação

## ⚡ Mecânicas Avançadas

### **Combinação de Power-ups**
- Múltiplos power-ups podem estar ativos simultaneamente
- Os efeitos se multiplicam entre si
- Exemplo: Turbo + Câmera Lenta = Movimento rápido com obstáculos lentos

### **Sistema de Ímã**
- Power-ups próximos são atraídos automaticamente
- Funciona mesmo se você não se mover
- Útil para coletar power-ups que estão em faixas diferentes

### **Efeitos Visuais**
- Power-ups rotacionam e pulsam
- Cores específicas para cada tipo
- Símbolos únicos para fácil identificação

## 📊 Estatísticas do Sistema

- **Chance de spawn**: 8% a cada 2 segundos
- **Intervalo de spawn**: 2.0 segundos
- **Total de tipos**: 5 power-ups diferentes
- **Duração média**: 5.2 segundos

## 🎯 Dicas de Estratégia

### **Para Iniciantes:**
1. Foque em coletar Escudos quando estiver em dificuldade
2. Use Ímãs para facilitar a coleta de outros power-ups
3. Pontos Duplos são mais valiosos em velocidades altas

### **Para Jogadores Avançados:**
1. Combine Turbo + Câmera Lenta para máxima eficiência
2. Use Escudo estrategicamente para passar por obstáculos impossíveis
3. Mantenha Pontos Duplos ativos durante sequências de obstáculos fáceis

### **Combinações Recomendadas:**
- **Defensiva**: Escudo + Ímã
- **Ofensiva**: Turbo + Pontos Duplos
- **Equilibrada**: Câmera Lenta + Ímã + Pontos Duplos

## 🔧 Configurações Técnicas

### **Arquivos Principais:**
- `src/config.py`: Configurações dos power-ups
- `src/entities/powerup.py`: Lógica dos power-ups
- `src/ui/hud.py`: Interface de ajuda
- `main_new.py`: Integração no jogo principal

### **Personalização:**
Você pode modificar os power-ups editando `src/config.py`:
- Alterar cores, durações e efeitos
- Adicionar novos tipos de power-ups
- Ajustar chances de spawn

## 🎨 Interface do Usuário

### **HUD Durante o Jogo:**
- Power-ups ativos aparecem no canto superior direito
- Tempo restante é mostrado para cada power-up
- Cores correspondem aos tipos de power-ups

### **Tela de Ajuda:**
- Lista completa de todos os power-ups
- Estatísticas do sistema
- Dicas de estratégia
- Símbolos visuais para cada tipo

## 🚀 Futuras Melhorias

### **Possíveis Adições:**
- Power-ups raros com efeitos especiais
- Sistema de combos para power-ups
- Power-ups negativos (desafio)
- Power-ups específicos para carros da polícia
- Sistema de conquistas baseado em power-ups

### **Melhorias de Interface:**
- Animações mais elaboradas
- Efeitos sonoros específicos
- Indicadores visuais de alcance do ímã
- Histórico de power-ups coletados

---

**🎮 Divirta-se explorando todas as possibilidades do sistema de power-ups!** 