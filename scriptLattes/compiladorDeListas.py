#!/usr/bin/python
# encoding: utf-8
#
#
#  scriptLattes
#  http://scriptlattes.sourceforge.net/
#
#
#  Este programa é um software livre; você pode redistribui-lo e/ou
#  modifica-lo dentro dos termos da Licença Pública Geral GNU como
#  publicada pela Fundação do Software Livre (FSF); na versão 2 da
#  Licença, ou (na sua opinião) qualquer versão.
#
#  Este programa é distribuído na esperança que possa ser util,
#  mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#  MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
#  Licença Pública Geral GNU para maiores detalhes.
#
#  Você deve ter recebido uma cópia da Licença Pública Geral GNU
#  junto com este programa, se não, escreva para a Fundação do Software
#  Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#

import operator
import re
from scipy import sparse
from scriptLattes.util import merge_dols

class CompiladorDeListas:
    grupo = None
    matrizArtigoEmPeriodico = None
    matrizLivroPublicado = None
    matrizCapituloDeLivroPublicado = None
    matrizTextoEmJornalDeNoticia = None
    matrizTrabalhoCompletoEmCongresso = None
    matrizResumoExpandidoEmCongresso = None
    matrizResumoEmCongresso = None
    matrizArtigoAceito = None
    matrizApresentacaoDeTrabalho = None
    matrizOutroTipoDeProducaoBibliografica = None

    def __init__(self, grupo):
        self.grupo = grupo

        self.listaCompletaPB = {}
        self.listaCompletaPT = {}
        self.listaCompletaPR = {}
        self.listaCompletaPA = {}
        self.listaCompletaOA = {}
        self.listaCompletaOC = {}

        self.listaCompletaArtigoEmPeriodico = {}
        self.listaCompletaLivroPublicado = {}
        self.listaCompletaCapituloDeLivroPublicado = {}
        self.listaCompletaTextoEmJornalDeNoticia = {}
        self.listaCompletaTrabalhoCompletoEmCongresso = {}
        self.listaCompletaResumoExpandidoEmCongresso = {}
        self.listaCompletaResumoEmCongresso = {}
        self.listaCompletaArtigoAceito = {}
        self.listaCompletaApresentacaoDeTrabalho = {}
        self.listaCompletaOutroTipoDeProducaoBibliografica = {}

        self.listaCompletaParticipacaoEmEvento = {}
        self.listaCompletaOrganizacaoDeEvento = {}


        # compilamos as producoes de todos os membros (separados por tipos)
        for membro in grupo.listaDeMembros:
            self.listaCompletaArtigoEmPeriodico = self.compilarLista(membro.listaArtigoEmPeriodico,
                                                                     self.listaCompletaArtigoEmPeriodico)
            self.listaCompletaLivroPublicado = self.compilarLista(membro.listaLivroPublicado,
                                                                  self.listaCompletaLivroPublicado)
            self.listaCompletaCapituloDeLivroPublicado = self.compilarLista(membro.listaCapituloDeLivroPublicado,
                                                                            self.listaCompletaCapituloDeLivroPublicado)
            self.listaCompletaTextoEmJornalDeNoticia = self.compilarLista(membro.listaTextoEmJornalDeNoticia,
                                                                          self.listaCompletaTextoEmJornalDeNoticia)
            self.listaCompletaTrabalhoCompletoEmCongresso = self.compilarLista(membro.listaTrabalhoCompletoEmCongresso,
                                                                               self.listaCompletaTrabalhoCompletoEmCongresso)
            self.listaCompletaResumoExpandidoEmCongresso = self.compilarLista(membro.listaResumoExpandidoEmCongresso,
                                                                              self.listaCompletaResumoExpandidoEmCongresso)
            self.listaCompletaResumoEmCongresso = self.compilarLista(membro.listaResumoEmCongresso,
                                                                     self.listaCompletaResumoEmCongresso)
            self.listaCompletaArtigoAceito = self.compilarLista(membro.listaArtigoAceito,
                                                                self.listaCompletaArtigoAceito)
            self.listaCompletaApresentacaoDeTrabalho = self.compilarLista(membro.listaApresentacaoDeTrabalho,
                                                                          self.listaCompletaApresentacaoDeTrabalho)
            self.listaCompletaOutroTipoDeProducaoBibliografica = self.compilarLista(
                membro.listaOutroTipoDeProducaoBibliografica, self.listaCompletaOutroTipoDeProducaoBibliografica)


            self.listaCompletaParticipacaoEmEvento = self.compilarLista(membro.listaParticipacaoEmEvento,
                                                                        self.listaCompletaParticipacaoEmEvento)
            self.listaCompletaOrganizacaoDeEvento = self.compilarLista(membro.listaOrganizacaoDeEvento,
                                                                       self.listaCompletaOrganizacaoDeEvento)

        # ---------------------------------------------------------------------------
        # compilamos as producoes de todos os tipos
        if self.grupo.obterParametro('relatorio-incluir_artigo_em_periodico'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaArtigoEmPeriodico,
                                                                self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_livro_publicado'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaLivroPublicado, self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_capitulo_de_livro_publicado'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaCapituloDeLivroPublicado,
                                                                self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_texto_em_jornal_de_noticia'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaTextoEmJornalDeNoticia,
                                                                self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_trabalho_completo_em_congresso'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaTrabalhoCompletoEmCongresso,
                                                                self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_resumo_expandido_em_congresso'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaResumoExpandidoEmCongresso,
                                                                self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_resumo_em_congresso'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaResumoEmCongresso,
                                                                self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_artigo_aceito_para_publicacao'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaArtigoAceito, self.listaCompletaPB)
        if self.grupo.obterParametro('relatorio-incluir_apresentacao_de_trabalho'):
            self.listaCompletaPB = self.compilarListasCompletas(self.listaCompletaApresentacaoDeTrabalho,
                                                                self.listaCompletaPB)




        for membro in grupo.listaDeMembros:
            if membro.idLattes == '0000000000000000':
                print ":: Processando coautor sem CV-Lattes" + membro.nomeInicial

                self.adicionarCoautorNaLista(self.listaCompletaArtigoEmPeriodico, membro)
                self.adicionarCoautorNaLista(self.listaCompletaArtigoEmPeriodico, membro)

                self.adicionarCoautorNaLista(self.listaCompletaLivroPublicado, membro)
                self.adicionarCoautorNaLista(self.listaCompletaCapituloDeLivroPublicado, membro)
                self.adicionarCoautorNaLista(self.listaCompletaTextoEmJornalDeNoticia, membro)
                self.adicionarCoautorNaLista(self.listaCompletaTrabalhoCompletoEmCongresso, membro)
                self.adicionarCoautorNaLista(self.listaCompletaResumoExpandidoEmCongresso, membro)
                self.adicionarCoautorNaLista(self.listaCompletaResumoEmCongresso, membro)
                self.adicionarCoautorNaLista(self.listaCompletaArtigoAceito, membro)
                self.adicionarCoautorNaLista(self.listaCompletaApresentacaoDeTrabalho, membro)
                self.adicionarCoautorNaLista(self.listaCompletaOutroTipoDeProducaoBibliografica, membro)





    def adicionarCoautorNaLista(self, listaCompleta, membro):
        keys = listaCompleta.keys()
        for ano in keys:
            for pub in listaCompleta[ano]:
                if self.procuraNomeEmPublicacao(membro.nomeInicial, pub.autores):
                    pub.idMembro.add(membro.idMembro)
                    # print ">>>" + membro.nomeInicial
                    #print ">>>" + pub.autores


    def procuraNomeEmPublicacao(self, nomesAbreviados, nomesDosCoautores):
        nomesAbreviados = nomesAbreviados.lower()
        nomesDosCoautores = nomesDosCoautores.lower()

        nomesAbreviados = nomesAbreviados.replace(".", " ")
        nomesDosCoautores = nomesDosCoautores.replace(".", " ")
        nomesDosCoautores = nomesDosCoautores.replace(",", " ")
        nomesAbreviados = re.sub('\s+', ' ', nomesAbreviados).strip()
        nomesDosCoautores = re.sub('\s+', ' ', nomesDosCoautores).strip()

        listaNomesAbreviados = nomesAbreviados.split(";")
        listaNomesDosCoautores = nomesDosCoautores.split(";")

        for abrev1 in listaNomesAbreviados:
            abrev1 = abrev1.strip()
            for abrev2 in listaNomesDosCoautores:
                abrev2 = abrev2.strip()
                if abrev1 == abrev2 and len(abrev1) > 0 and len(abrev2) > 0:
                    return True
        return False


    def compilarLista(self, listaDoMembro, listaCompleta):
        for pub in listaDoMembro:  # adicionar 'pub'  em  'listaCompleta'
            if pub == None or listaCompleta.get(pub.ano) == None:  # Se o ano nao existe no listaCompleta (lista total)
                listaCompleta[pub.ano] = []  # criamos uma nova entrada vazia
                listaCompleta[pub.ano].append(pub)
            else:
                inserir = 1
                for i in range(0, len(listaCompleta[pub.ano])):
                    item = pub.compararCom(listaCompleta[pub.ano][i])  # comparamos: pub com listaCompleta[pub.ano][i]
                    if not item == None:  # sao similares
                        print "\n[AVISO] PRODUÇÕES SIMILARES",
                        print pub,
                        print listaCompleta[pub.ano][i]
                        # print "Membro " + str(pub.idMembro) + ": " + pub.titulo.encode('utf8')
                        # print "Membro " + str(listaCompleta[pub.ano][i].idMembro) + ": " + listaCompleta[pub.ano][i].titulo.encode('utf8')

                        listaCompleta[pub.ano][i] = item
                        inserir = 0
                        break
                if inserir:  # se pub for difererente a todos os elementos do listaCompleta
                    listaCompleta[pub.ano].append(pub)
        return listaCompleta

    # Para projetos não é feita a busca de projetos similares (NÃO MAIS UTILIZADA)
    def compilarListaDeProjetos(self, listaDoMembro, listaCompleta):
        for pub in listaDoMembro:  # adicionar 'pub'  em  'listaCompleta'
            if listaCompleta.get(pub.anoInicio) == None:
                listaCompleta[pub.anoInicio] = []
            listaCompleta[pub.anoInicio].append(pub)
        return listaCompleta

    def compilarListasCompletas(self, listaCompleta, listaTotal):
        keys = listaCompleta.keys()
        for ano in keys:
            if listaTotal.get(ano) == None:
                listaTotal[ano] = []
            listaTotal[ano].extend(listaCompleta[ano])
        return listaTotal


    def criarMatrizesDeColaboracao(self):
        if self.grupo.obterParametro('grafo-incluir_artigo_em_periodico'):
            self.matrizesArtigoEmPeriodico = self.criarMatrizes(self.listaCompletaArtigoEmPeriodico)
        if self.grupo.obterParametro('grafo-incluir_livro_publicado'):
            self.matrizesLivroPublicado = self.criarMatrizes(self.listaCompletaLivroPublicado)
        if self.grupo.obterParametro('grafo-incluir_capitulo_de_livro_publicado'):
            self.matrizesCapituloDeLivroPublicado = self.criarMatrizes(self.listaCompletaCapituloDeLivroPublicado)
        if self.grupo.obterParametro('grafo-incluir_texto_em_jornal_de_noticia'):
            self.matrizesTextoEmJornalDeNoticia = self.criarMatrizes(self.listaCompletaTextoEmJornalDeNoticia)
        if self.grupo.obterParametro('grafo-incluir_trabalho_completo_em_congresso'):
            self.matrizesTrabalhoCompletoEmCongresso = self.criarMatrizes(self.listaCompletaTrabalhoCompletoEmCongresso)
        if self.grupo.obterParametro('grafo-incluir_resumo_expandido_em_congresso'):
            self.matrizesResumoExpandidoEmCongresso = self.criarMatrizes(self.listaCompletaResumoExpandidoEmCongresso)
        if self.grupo.obterParametro('grafo-incluir_resumo_em_congresso'):
            self.matrizesResumoEmCongresso = self.criarMatrizes(self.listaCompletaResumoEmCongresso)
        if self.grupo.obterParametro('grafo-incluir_artigo_aceito_para_publicacao'):
            self.matrizesArtigoAceito = self.criarMatrizes(self.listaCompletaArtigoAceito)
        if self.grupo.obterParametro('grafo-incluir_apresentacao_de_trabalho'):
            self.matrizesApresentacaoDeTrabalho = self.criarMatrizes(self.listaCompletaApresentacaoDeTrabalho)
        if self.grupo.obterParametro('grafo-incluir_outro_tipo_de_producao_bibliografica'):
            self.matrizesOutroTipoDeProducaoBibliografica = self.criarMatrizes(self.listaCompletaOutroTipoDeProducaoBibliografica)




        # Criamos as matrizes de:
        #  - (1) adjacência
        #  - (2) frequencia

    def criarMatrizes(self, listaCompleta):
        # matriz1 = numpy.zeros((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()), dtype=numpy.int32)
        # matriz2 = numpy.zeros((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()), dtype=numpy.float32)
        matriz1 = sparse.lil_matrix((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()))
        matriz2 = sparse.lil_matrix((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()))

        # armazenamos a lista de itens associadas a cada colaboracao endogena
        listaDeColaboracoes = list([])
        for i in range(0, self.grupo.numeroDeMembros()):
            listaDeColaboracoes.append( dict([]) )

        keys = listaCompleta.keys()
        keys.sort(reverse=True)
        for k in keys:
            for pub in listaCompleta[k]:

                numeroDeCoAutores = len(pub.idMembro)
                if numeroDeCoAutores > 1:
                    # Para todos os co-autores da publicacao:
                    # (1) atualizamos o contador de colaboracao (adjacencia)
                    # (2) incrementamos a 'frequencia' de colaboracao
                    combinacoes = self.calcularCombinacoes(pub.idMembro)
                    for c in combinacoes:
                        matriz1[c[0], c[1]] += 1
                        matriz1[c[1], c[0]] += 1
                        matriz2[c[0], c[1]] += 1.0 / (numeroDeCoAutores - 1)
                        matriz2[c[1], c[0]] += 1.0 / (numeroDeCoAutores - 1)

                        if not c[0] in listaDeColaboracoes[c[1]]:
                            listaDeColaboracoes[c[1]][ c[0] ] = list([])
                        if not c[1] in listaDeColaboracoes[c[0]]:
                            listaDeColaboracoes[c[0]][ c[1] ] = list([])

                        listaDeColaboracoes[c[0]][ c[1] ].append(pub)
                        listaDeColaboracoes[c[1]][ c[0] ].append(pub)

        return [matriz1, matriz2, listaDeColaboracoes]


    # combinacoes 2 a 2 de todos os co-autores da publicação
    # exemplo:
    # lista = [0, 3, 1]
    # combinacoes = [[0,3], [0,1], [3,1]]
    def calcularCombinacoes(self, conjunto):
        lista = list(conjunto)
        combinacoes = []
        for i in range(0, len(lista) - 1):
            for j in range(i + 1, len(lista)):
                combinacoes.append([lista[i], lista[j]])
        return combinacoes


    def intercalar_colaboracoes(self, lista1, lista2):
        for i in range(0, self.grupo.numeroDeMembros()):
            lista1[i] = merge_dols( lista1[i], lista2[i] )
        return lista1


    def uniaoDeMatrizesDeColaboracao(self):
        ##matriz1 = numpy.zeros((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()), dtype=numpy.int32)
        ##matriz2 = numpy.zeros((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()), dtype=numpy.float32)
        matriz1 = sparse.lil_matrix((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()))
        matriz2 = sparse.lil_matrix((self.grupo.numeroDeMembros(), self.grupo.numeroDeMembros()))
        colaboracoes = []
        for i in range(0, self.grupo.numeroDeMembros()):
            colaboracoes.append([])

        if self.grupo.obterParametro('grafo-incluir_artigo_em_periodico'):
            matriz1 += self.matrizesArtigoEmPeriodico[0]
            matriz2 += self.matrizesArtigoEmPeriodico[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesArtigoEmPeriodico[2] )
        if self.grupo.obterParametro('grafo-incluir_livro_publicado'):
            matriz1 += self.matrizesLivroPublicado[0]
            matriz2 += self.matrizesLivroPublicado[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesLivroPublicado[2] )
        if self.grupo.obterParametro('grafo-incluir_capitulo_de_livro_publicado'):
            matriz1 += self.matrizesCapituloDeLivroPublicado[0]
            matriz2 += self.matrizesCapituloDeLivroPublicado[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesCapituloDeLivroPublicado[2] )
        if self.grupo.obterParametro('grafo-incluir_texto_em_jornal_de_noticia'):
            matriz1 += self.matrizesTextoEmJornalDeNoticia[0]
            matriz2 += self.matrizesTextoEmJornalDeNoticia[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesTextoEmJornalDeNoticia[2] )
        if self.grupo.obterParametro('grafo-incluir_trabalho_completo_em_congresso'):
            matriz1 += self.matrizesTrabalhoCompletoEmCongresso[0]
            matriz2 += self.matrizesTrabalhoCompletoEmCongresso[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesTrabalhoCompletoEmCongresso[2] )
        if self.grupo.obterParametro('grafo-incluir_resumo_expandido_em_congresso'):
            matriz1 += self.matrizesResumoExpandidoEmCongresso[0]
            matriz2 += self.matrizesResumoExpandidoEmCongresso[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesResumoExpandidoEmCongresso[2] )
        if self.grupo.obterParametro('grafo-incluir_resumo_em_congresso'):
            matriz1 += self.matrizesResumoEmCongresso[0]
            matriz2 += self.matrizesResumoEmCongresso[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesResumoEmCongresso[2] )
        if self.grupo.obterParametro('grafo-incluir_artigo_aceito_para_publicacao'):
            matriz1 += self.matrizesArtigoAceito[0]
            matriz2 += self.matrizesArtigoAceito[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesArtigoAceito[2] )
        if self.grupo.obterParametro('grafo-incluir_apresentacao_de_trabalho'):
            matriz1 += self.matrizesApresentacaoDeTrabalho[0]
            matriz2 += self.matrizesApresentacaoDeTrabalho[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesApresentacaoDeTrabalho[2] )
        if self.grupo.obterParametro('grafo-incluir_outro_tipo_de_producao_bibliografica'):
            matriz1 += self.matrizesOutroTipoDeProducaoBibliografica[0]
            matriz2 += self.matrizesOutroTipoDeProducaoBibliografica[1]
            colaboracoes = self.intercalar_colaboracoes( colaboracoes, self.matrizesOutroTipoDeProducaoBibliografica[2] )




        return [matriz1, matriz2, colaboracoes]


    def imprimirMatrizesDeFrequencia(self):
        print "\n[LISTA DE MATRIZES DE FREQUENCIA]"
        print "\nArtigo em periodico"
        print self.matrizArtigoEmPeriodico
        print "\nLivro publicado"
        print self.matrizLivroPublicado
        print "\nCapitulo de livro publicado"
        print self.matrizCapituloDeLivroPublicado
        print "\nTexto em jornal de noticia"
        print self.matrizTextoEmJornalDeNoticia
        print "\nTrabalho completo em congresso"
        print self.matrizTrabalhoCompletoEmCongresso
        print "\nResumo expandido em congresso"
        print self.matrizResumoExpandidoEmCongresso
        print "\nResumo em congresso"
        print self.matrizResumoEmCongresso
        print "\nArtigo aceito"
        print self.matrizArtigoAceito
        print "\nApresentacao de trabalho"
        print self.matrizApresentacaoDeTrabalho
        print "\nOutro tipo de producao bibliografica"
        print self.matrizOutroTipoDeProducaoBibliografica

    def imprimirListasCompletas(self):
        print "\n\n[LISTA COMPILADA DE PRODUÇÕES]"

        print "\nArtigo em periodico"
        self.imprimirListaProducoes(self.listaCompletaArtigoEmPeriodico)
        print "\nLivro publicado"
        self.imprimirListaProducoes(self.listaCompletaLivroPublicado)
        print "\nCapitulo de livro publicado"
        self.imprimirListaProducoes(self.listaCompletaCapituloDeLivroPublicado)
        print "\nTexto em jornal de noticia"
        self.imprimirListaProducoes(self.listaCompletaTextoEmJornalDeNoticia)
        print "\nTrabalho completo em congresso"
        self.imprimirListaProducoes(self.listaCompletaTrabalhoCompletoEmCongresso)
        print "\nResumo expandido em congresso"
        self.imprimirListaProducoes(self.listaCompletaResumoExpandidoEmCongresso)
        print "\nResumo em congresso"
        self.imprimirListaProducoes(self.listaCompletaResumoEmCongresso)
        print "\nArtigo aceito"
        self.imprimirListaProducoes(self.listaCompletaArtigoAceito)
        print "\nApresentacao de trabalho"
        self.imprimirListaProducoes(self.listaCompletaApresentacaoDeTrabalho)
        print "\nOutro tipo de producao bibliografica"
        self.imprimirListaProducoes(self.listaCompletaOutroTipoDeProducaoBibliografica)
        print "\nTOTAL DE PB"
        self.imprimirListaProducoes(self.listaCompletaPB)

        self.imprimirListaProducoes(self.listaCompletaPR)



    def imprimirListaProducoes(self, listaCompleta):
        print "---------------------------------------------------------------------------"
        keys = listaCompleta.keys()
        keys.sort(reverse=True)
        for k in keys:
            print k
            listaCompleta[k].sort(key=operator.attrgetter('autores'))

            for pub in listaCompleta[k]:
                print "--- " + str(pub.idMembro)
                print "--- " + pub.autores.encode('utf8')
                print "--- " + pub.titulo.encode('utf8') + "\n"


    def imprimirListaOrientacoes(self, listaCompleta):
        print "---------------------------------------------------------------------------"
        keys = listaCompleta.keys()
        keys.sort(reverse=True)
        for k in keys:
            print k
            listaCompleta[k].sort(key=operator.attrgetter('nome'))

            for pub in listaCompleta[k]:
                print "--- " + str(pub.idMembro)
                print "--- " + pub.nome.encode('utf8')
                print "--- " + pub.tituloDoTrabalho.encode('utf8') + "\n"
