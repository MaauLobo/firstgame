# -*- coding: utf-8 -*-
"""
Gerenciador de record (melhor pontuação)
"""

import os
from ..config import RECORD_FILE


class RecordManager:
    def __init__(self):
        self.record_atual = 0
        self.carregar_record()
    
    def carregar_record(self):
        """Carrega o record do arquivo"""
        try:
            if os.path.exists(RECORD_FILE):
                with open(RECORD_FILE, 'r') as arquivo:
                    conteudo = arquivo.read().strip()
                    if conteudo.isdigit():
                        self.record_atual = int(conteudo)
                        print(f"🏆 Record carregado: {self.record_atual}")
                    else:
                        print("⚠️ Arquivo de record corrompido, iniciando com 0")
                        self.record_atual = 0
            else:
                print("📝 Nenhum record encontrado, iniciando com 0")
                self.record_atual = 0
        except Exception as e:
            print(f"❌ Erro ao carregar record: {e}")
            self.record_atual = 0
    
    def salvar_record(self):
        """Salva o record atual no arquivo"""
        try:
            with open(RECORD_FILE, 'w') as arquivo:
                arquivo.write(str(self.record_atual))
            print(f"💾 Record salvo: {self.record_atual}")
        except Exception as e:
            print(f"❌ Erro ao salvar record: {e}")
    
    def verificar_novo_record(self, pontuacao):
        """Verifica se a pontuação é um novo record"""
        if pontuacao > self.record_atual:
            self.record_atual = pontuacao
            self.salvar_record()
            return True
        return False
    
    def obter_record(self):
        """Retorna o record atual"""
        return self.record_atual
    
    def resetar_record(self):
        """Reseta o record para 0"""
        self.record_atual = 0
        self.salvar_record()
        print("🔄 Record resetado para 0") 