# 🏎️ Velozes e Assados

## 📋 Informações do Projeto

**Desenvolvedor:** Mauricio Lobo Lima  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Disciplina:** Desenvolvimento de Jogos  
**Data:** 2024  
**Motor:** Pygame  
**Linguagem:** Python  

---

## 🎮 Sobre o Jogo

"Velozes e Assados" é um jogo de corrida em terceira pessoa onde o jogador controla um carro em uma estrada infinita, desviando de obstáculos e tentando sobreviver o máximo tempo possível. O jogo combina elementos de arcade clássico com mecânicas modernas como sistema de playlist dinâmica, IA inteligente para carros da polícia e um sistema completo de power-ups.

### ✨ Características Principais

- **Sistema de Power-ups**: 5 tipos diferentes com efeitos únicos
- **Playlist Dinâmica**: Controle total da música durante o jogo
- **IA da Polícia**: Carros da polícia com comportamento inteligente
- **Sistema de Pontuação**: Progressão infinita com dificuldade escalável
- **Interface Moderna**: HUD informativo e tela de ajuda integrada

---

## 🚀 Como Iniciar o Jogo

### 📋 Pré-requisitos

1. **Python 3.7+** instalado no seu computador
2. **Pygame 2.0+** instalado
3. **Sistema Operacional**: Windows, Linux ou macOS

### 🔧 Instalação

#### **Passo 1: Verificar Python**
```bash
python --version
# Deve mostrar Python 3.7 ou superior
```

#### **Passo 2: Instalar Pygame**
```bash
pip install pygame
```

#### **Passo 3: Baixar o Projeto**
```bash
# Se você já tem o projeto, pule esta etapa
git clone [URL_DO_REPOSITORIO]
cd firstgame
```

#### **Passo 4: Verificar Estrutura**
Certifique-se de que a estrutura de pastas está correta:
```
firstgame/
├── main_new.py          # Arquivo principal
├── src/                 # Código fonte
├── assets/              # Recursos do jogo
│   ├── images/          # Imagens
│   ├── sounds/          # Sons e músicas
│   └── videos/          # Vídeos
└── README.md           # Este arquivo
```

### 🎮 Executando o Jogo

#### **Método Simples:**
```bash
python main_new.py
```

#### **Método com Verificação:**
```bash
# Verificar se todas as dependências estão instaladas
pip install -r requirements.txt

# Executar o jogo
python main_new.py
```

---

## 🎯 Controles do Jogo

### **Controles Principais**
- **Setas Esquerda/Direita** ou **A/D**: Movimento lateral do carro
- **ESPAÇO**: Iniciar jogo (menu)
- **R**: Reiniciar após game over
- **H**: Mostrar ajuda dos power-ups

### **Controles da Playlist (Durante o Jogo)**
- **N**: Próxima música
- **R**: Música aleatória
- **P**: Pausar/Despausar música
- **M**: Mudo/Desmudo
- **+/-**: Ajustar volume
- **0**: Resetar volume para 20%

### **Controles Adicionais**
- **F1**: Resetar record
- **ESC**: Pausar jogo

---

## 🎁 Sistema de Power-ups

O jogo possui 5 tipos de power-ups que podem ser coletados na estrada:

### **🛡️ Escudo (Ciano)**
- **Duração**: 5 segundos
- **Efeito**: Imunidade total contra colisões

### **⚡ Turbo (Amarelo)**
- **Duração**: 3 segundos
- **Efeito**: Aumenta velocidade do jogador em 50%

### **⏰ Câmera Lenta (Roxo)**
- **Duração**: 4 segundos
- **Efeito**: Reduz velocidade dos obstáculos em 50%

### **🧲 Ímã (Magenta)**
- **Duração**: 6 segundos
- **Efeito**: Atrai power-ups próximos automaticamente

### **💎 Pontos Duplos (Verde)**
- **Duração**: 8 segundos
- **Efeito**: Duplica a pontuação ganha

---

## 🎵 Sistema de Áudio

### **Música de Abertura**
- Arquivo: `assets/sounds/abertura.mp3`
- Volume inicial: 20%

### **Playlist do Jogo**
- Localização: `assets/sounds/playlist/`
- Formatos suportados: MP3, WAV, OGG
- Volume inicial: 20%
- Controle total pelo jogador

---

## 🛠️ Solução de Problemas

### **Erro: "pygame module not found"**
```bash
pip install pygame
```

### **Erro: "No module named 'src'"**
Certifique-se de estar executando o jogo da pasta raiz do projeto:
```bash
cd firstgame
python main_new.py
```

### **Erro: "File not found"**
Verifique se a estrutura de pastas está correta e se todos os arquivos de assets estão presentes.

### **Música não toca**
- Verifique se os arquivos de música estão na pasta `assets/sounds/playlist/`
- Verifique se o volume do sistema não está mutado
- Use as teclas +/- para ajustar o volume

### **Jogo muito lento**
- Feche outros programas que consomem muita memória
- Verifique se o Python e Pygame estão atualizados
- Reduza a resolução do sistema se necessário

---

## 📁 Estrutura do Projeto

```
firstgame/
├── main_new.py              # Arquivo principal do jogo
├── src/                     # Código fonte
│   ├── config.py           # Configurações e constantes
│   ├── game_states.py      # Gerenciamento de estados
│   ├── entities/           # Entidades do jogo
│   │   ├── player.py       # Carro do jogador
│   │   ├── obstacles.py    # Obstáculos
│   │   ├── police.py       # Carros da polícia
│   │   └── powerup.py      # Sistema de power-ups
│   ├── managers/           # Gerenciadores
│   │   ├── playlist.py     # Sistema de música
│   │   ├── collision.py    # Detecção de colisão
│   │   └── record.py       # Sistema de record
│   ├── ui/                 # Interface do usuário
│   │   └── hud.py          # HUD e telas
│   └── utils/              # Utilitários
├── assets/                 # Recursos do jogo
│   ├── images/             # Imagens e sprites
│   ├── sounds/             # Sons e músicas
│   └── videos/             # Vídeos (cinemática)
├── requirements.txt        # Dependências Python
├── POWERUPS_GUIDE.md      # Guia detalhado dos power-ups
└── README.md              # Este arquivo
```

---

## 🎯 Objetivos do Jogo

- **Sobreviver** o máximo tempo possível
- **Desviar** de obstáculos e carros da polícia
- **Coletar** power-ups para obter vantagens
- **Atingir** a maior pontuação possível
- **Quebrar** seu record pessoal

---

## 🏆 Sistema de Pontuação

- **1 ponto** por obstáculo evitado
- **Multiplicadores** através de power-ups
- **Record** salvo automaticamente
- **Progressão** infinita com dificuldade crescente

---

## 📞 Suporte

Se encontrar problemas ou tiver dúvidas:

1. Verifique se seguiu todos os passos de instalação
2. Consulte a seção "Solução de Problemas"
3. Verifique se todas as dependências estão instaladas
4. Teste com diferentes arquivos de música

---

**🎮 Divirta-se jogando "Velozes e Assados"!**

