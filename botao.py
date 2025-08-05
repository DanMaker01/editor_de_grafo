import pygame

class Botao:
    def __init__(self, texto, pos, tamanho, callback, fonte=None, cor_fundo=(70, 70, 70), cor_hover=(100, 100, 100), cor_texto=(255, 255, 255)):
        self.texto = texto
        self.pos = pos  # (x, y)
        self.tamanho = tamanho  # (largura, altura)
        self.callback = callback
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.fonte = fonte or pygame.font.SysFont(None, 24)
        self.rect = pygame.Rect(pos, tamanho)
        self.hovering = False

    def desenhar(self, tela):
        cor = self.cor_hover if self.hovering else self.cor_fundo
        pygame.draw.rect(tela, cor, self.rect)
        pygame.draw.rect(tela, (200, 200, 200), self.rect, 2)  # borda
        texto_renderizado = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        tela.blit(texto_renderizado, texto_rect)

    def handle_event(self, evento):  # Renomeado de verificar_evento para padronizar
        if evento.type == pygame.MOUSEMOTION:
            self.hovering = self.rect.collidepoint(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.hovering and evento.button == 1:
                self.callback()