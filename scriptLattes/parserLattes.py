#!/usr/bin/python
#  encoding: utf-8

import sys
from htmlentitydefs import name2codepoint
from tidylib import tidy_document


# ---------------------------------------------------------------------------- #
from HTMLParser import HTMLParser
from producoesUnitarias.formacaoAcademica import *
from producoesUnitarias.areaDeAtuacao import *
from producoesUnitarias.idioma import *
from producoesBibliograficas.artigoEmPeriodico import *
from producoesBibliograficas.trabalhoCompletoEmCongresso import *
from producoesBibliograficas.resumoExpandidoEmCongresso import *
from producoesBibliograficas.resumoEmCongresso import *


sys.tracebacklimit = 0

class ParserLattes(HTMLParser):

    identificador16 = ''
    item = None
    nomeCompleto = ''
    bolsaProdutividade = ''
    enderecoProfissional = ''
    sexo = ''
    nomeEmCitacoesBibliograficas = ''
    atualizacaoCV = ''
    foto = ''
    textoResumo = ''


    salvarIdentificador16 = None
    salvarNome = None
    salvarBolsaProdutividade = None
    salvarEnderecoProfissional = None
    salvarSexo = None
    salvarNomeEmCitacoes = None
    salvarAtualizacaoCV = None
    salvarTextoResumo = None
    salvarFormacaoAcademica = None
    salvarAreaDeAtuacao = None
    salvarIdioma = None
    salvarItem = None
    salvarParticipacaoEmEvento = None
    salvarOrganizacaoDeEvento = None

    # novos atributos
    achouIdentificacao = None
    achouEndereco = None
    salvarParte1 = None
    salvarParte2 = None
    salvarParte3 = None
    achouProducoes = None
    achouProducaoEmCTA = None

    achouBancas = None

    achouOutrasInformacoesRelevantes = None
    spanInformacaoArtigo = None

    recuperarIdentificador16 = None


    achouGrupo = None
    achouEnderecoProfissional = None
    achouSexo = None
    achouNomeEmCitacoes = None
    achouFormacaoAcademica = None
    achouAreaDeAtuacao = None
    achouIdioma = None

    achouArtigoEmPeriodico = None
    achouLivroPublicado = None
    achouCapituloDeLivroPublicado = None
    achouTextoEmJornalDeNoticia = None
    achouTrabalhoCompletoEmCongresso = None
    achouResumoExpandidoEmCongresso = None
    achouResumoEmCongresso = None
    achouArtigoAceito = None
    achouApresentacaoDeTrabalho = None
    achouOutroTipoDeProducaoBibliografica = None
    achouParticipacaoEmEvento = None
    achouOrganizacaoDeEvento = None

    procurarCabecalho = None
    partesDoItem = []

    listaIDLattesColaboradores = []
    listaFormacaoAcademica = []
    listaAreaDeAtuacao = []
    listaIdioma = []


    listaArtigoEmPeriodico = []
    listaLivroPublicado = []
    listaCapituloDeLivroPublicado = []
    listaTextoEmJornalDeNoticia = []
    listaTrabalhoCompletoEmCongresso = []
    listaResumoExpandidoEmCongresso = []
    listaResumoEmCongresso = []
    listaArtigoAceito = []
    listaApresentacaoDeTrabalho = []
    listaOutroTipoDeProducaoBibliografica = []


    # auxiliares
    doi = ''
    relevante = 0
    umaUnidade = 0
    idOrientando = None
    citado = 0
    complemento = ''

    # ------------------------------------------------------------------------ #
    def __init__(self, idMembro, cvLattesHTML):
        HTMLParser.__init__(self)

        # inicializacao obrigatoria
        self.idMembro = idMembro
        self.sexo = 'Masculino'
        self.nomeCompleto = u'[Nome-nao-identificado]'

        self.item = ''
        self.issn = ''
        self.listaIDLattesColaboradores = []
        self.listaFormacaoAcademica = []
        self.listaAreaDeAtuacao = []
        self.listaIdioma = []

        self.listaArtigoEmPeriodico = []
        self.listaLivroPublicado = []
        self.listaCapituloDeLivroPublicado = []
        self.listaTextoEmJornalDeNoticia = []
        self.listaTrabalhoCompletoEmCongresso = []
        self.listaResumoExpandidoEmCongresso = []
        self.listaResumoEmCongresso = []
        self.listaArtigoAceito = []
        self.listaApresentacaoDeTrabalho = []
        self.listaOutroTipoDeProducaoBibliografica = []


        self.listaParticipacaoEmEvento = []
        self.listaOrganizacaoDeEvento = []


        # inicializacao para evitar a busca exaustiva de algumas palavras-chave
        self.salvarAtualizacaoCV = 1
        self.salvarFoto = 1
        self.procurarCabecalho = 0
        self.achouGrupo = 0
        self.doi = ''
        self.relevante = 0
        self.idOrientando = ''
        self.complemento = ''

        # contornamos alguns erros do HTML da Plataforma Lattes
        cvLattesHTML = cvLattesHTML.replace("<![CDATA[","")
        cvLattesHTML = cvLattesHTML.replace("]]>","")
        cvLattesHTML = cvLattesHTML.replace("<x<","&lt;x&lt;")
        cvLattesHTML = cvLattesHTML.replace("<X<","&lt;X&lt;")

        # feed it!
        cvLattesHTML, errors = tidy_document(cvLattesHTML, options={'numeric-entities':1})

        self.feed(cvLattesHTML)

    # ------------------------------------------------------------------------ #

    def parse_issn(self,url):
        s = url.find('issn=')
        if s == -1:
            return None
        e = url.find('&',s)
        if e == -1:
            return None

        issnvalue = url[s:e].split('=')
        issn = issnvalue[1]
        if len(issn) < 8: return
        issn = issn[:8]
        self.issn = issn[0:4]+'-'+issn[4:8]

    def handle_starttag(self, tag, attributes):

        if tag=='h2':
            for name, value in attributes:
                if name=='class' and value=='nome':
                    self.salvarNome = 1
                    self.item = ''
                    break

        if tag=='li':
            self.recuperarIdentificador16 = 1

        if tag=='p':
            for name, value in attributes:
                if name=='class' and value=='resumo':
                    self.salvarTextoResumo = 1
                    self.item = ''
                    break

        if (tag=='br' or tag=='img') and self.salvarNome:
            self.nomeCompleto = stripBlanks(self.item)
            self.item = ''
            self.salvarNome = 0
            self.salvarBolsaProdutividade = 1

        if tag=='span' and self.salvarBolsaProdutividade:
            self.item = ''

        if tag=='div':
            self.citado = 0

            for name, value in attributes:
                if name == 'cvuri':
                    self.parse_issn(value)


            for name, value in attributes:
                if name=='class' and value=='title-wrapper':
                    self.umaUnidade = 1
                    break

            for name, value in attributes:
                if name=='class' and value=='layout-cell-pad-5':
                    if self.achouNomeEmCitacoes:
                        self.salvarNomeEmCitacoes = 1
                        self.item = ''

                    if self.achouSexo:
                        self.salvarSexo = 1
                        self.item = ''

                    if self.achouEnderecoProfissional:
                        self.salvarEnderecoProfissional = 1
                        self.item = ''

                    if self.salvarParte1:
                        self.salvarParte1 = 0
                        self.salvarParte2 = 1

                if name=='class' and value=='layout-cell-pad-5 text-align-right':
                    self.item = ''
                    if self.achouFormacaoAcademica or self.achouAtuacaoProfissional or self.achouMembroDeCorpoEditorial or self.achouRevisorDePeriodico or self.achouAreaDeAtuacao or self.achouIdioma or  self.salvarItem:
                        self.salvarParte1 = 1
                        self.salvarParte2 = 0
                        if not self.salvarParte3:
                            self.partesDoItem = []

                if name == 'class' and (value == 'citacoes' or value == 'citado'):
                    self.citado = 1

                if name == 'cvuri' and self.citado:
                    self.citado = 0
                    self.complemento = value.replace("/buscatextual/servletcitacoes?", "")


        if tag=='h1' and self.umaUnidade:
            self.procurarCabecalho = 1

            self.achouIdentificacao = 0
            self.achouEndereco = 0
            self.achouFormacaoAcademica = 0
            self.achouAtuacaoProfissional = 0
            self.achouMembroDeCorpoEditorial = 0
            self.achouRevisorDePeriodico = 0
            self.achouAreaDeAtuacao = 0
            self.achouIdioma = 0
            self.achouProducoes = 0
            #self.achouProducaoEmCTA = 0
            self.achouBancas = 0


            self.achouOutrasInformacoesRelevantes = 0
            self.salvarItem = 0


        if tag=='img':
            if self.salvarFoto:
                for name, value in attributes:
                    if name=='src' and u'servletrecuperafoto' in value:
                        self.foto = value
                        self.salvarFoto = 0
                        break

            if self.salvarItem:
                for name, value in attributes:
                    if name=='src' and u'ico_relevante' in value:
                        self.relevante = 1
                        break

                """for name,value in attributes:
                    if name=='data-issn':
                        if len(value) == 8:
                            self.issn = value[0:4]+'-'+value[4:8]
                        break
                """




        if tag=='br':
            self.item = self.item + ' '

        if tag=='span':
            if self.achouProducaoEmCTA:
                for name, value in attributes:
                    if name=='class' and value==u'informacao-artigo':
                        self.spanInformacaoArtigo = 1

        if tag=='a':
            if self.salvarItem: # and self.achouArtigoEmPeriodico:
                for name, value in attributes:
                    if name=='href' and u'doi' in value:
                        self.doi = value
                        break

                    id = re.findall(u'http://lattes.cnpq.br/(\d{16})', value)
                    if name=='href' and len(id)>0:
                        self.listaIDLattesColaboradores.append(id[0])
                        break


    # ------------------------------------------------------------------------ #
    def handle_endtag(self, tag):

        if tag=='h2':
            if self.salvarNome:
                self.nomeCompleto = stripBlanks(self.item)
                self.salvarNome = 0
            if self.salvarBolsaProdutividade:
                self.salvarBolsaProdutividade = 0

        if tag=='p':
            if self.salvarTextoResumo:
                self.textoResumo = stripBlanks(self.item)
                self.salvarTextoResumo = 0

        if tag=='span' and self.salvarBolsaProdutividade:
            self.bolsaProdutividade = stripBlanks(self.item)
            self.bolsaProdutividade = re.sub('Bolsista de Produtividade em Pesquisa do CNPq - ','', self.bolsaProdutividade)
            self.bolsaProdutividade = self.bolsaProdutividade.strip('()')
            self.salvarBolsaProdutividade = 0

        if tag=='span' and self.salvarIdentificador16 == 1:
            self.identificador16 = re.findall(u'http://lattes.cnpq.br/(\d{16})', value)
            self.salvarIdentificador16 = 0


        if tag=='h1' and self.procurarCabecalho:
            self.procurarCabecalho = 0


        if tag=='div':
            if self.salvarNomeEmCitacoes:
                self.nomeEmCitacoesBibliograficas = stripBlanks(self.item)
                self.salvarNomeEmCitacoes = 0
                self.achouNomeEmCitacoes = 0
            if self.salvarSexo:
                self.sexo = stripBlanks(self.item)
                self.salvarSexo = 0
                self.achouSexo = 0
            if self.salvarEnderecoProfissional:
                self.enderecoProfissional = stripBlanks(self.item)
                self.enderecoProfissional = re.sub("\'", '', self.enderecoProfissional)
                self.enderecoProfissional = re.sub("\"", '', self.enderecoProfissional)
                self.salvarEnderecoProfissional = 0
                self.achouEnderecoProfissional = 0

            if (self.salvarParte1 and not self.salvarParte2) or (self.salvarParte2 and not self.salvarParte1) :
                if len(stripBlanks(self.item))>0:
                    self.partesDoItem.append(stripBlanks(self.item)) # acrescentamos cada celula da linha em uma lista!
                    self.item = ''

                if self.salvarParte2:
                    self.salvarParte1 = 0
                    self.salvarParte2 = 0

                    if self.achouFormacaoAcademica and len(self.partesDoItem)>=2:
                        iessimaFormacaoAcademica = FormacaoAcademica(self.partesDoItem)
                        self.listaFormacaoAcademica.append(iessimaFormacaoAcademica)

                    #if self.achouAtuacaoProfissional:
                    #	print self.partesDoItem


                    if self.achouAreaDeAtuacao and len(self.partesDoItem)>=2:
                        iessimaAreaDeAtucao = AreaDeAtuacao(self.partesDoItem)
                        self.listaAreaDeAtuacao.append(iessimaAreaDeAtucao) # acrescentamos o objeto de AreaDeAtuacao

                    if self.achouIdioma and len(self.partesDoItem)>=2:
                        iessimoIdioma = Idioma(self.partesDoItem)
                        self.listaIdioma.append(iessimoIdioma) # acrescentamos o objeto de Idioma


                    if self.achouProducoes:
                        if self.achouProducaoEmCTA:
                            if self.achouArtigoEmPeriodico:
                                iessimoItem = ArtigoEmPeriodico(self.idMembro, self.partesDoItem, self.doi,
                                                                self.relevante, self.complemento)
                                self.listaArtigoEmPeriodico.append(iessimoItem)
                                self.doi = ''
                                self.issn = ''
                                self.relevante = 0
                                self.complemento = ''


                            if self.achouTrabalhoCompletoEmCongresso:
                                iessimoItem = TrabalhoCompletoEmCongresso(self.idMembro, self.partesDoItem, self.doi,
                                                                          self.relevante)
                                self.listaTrabalhoCompletoEmCongresso.append(iessimoItem)
                                self.doi = ''
                                self.relevante = 0

                            if self.achouResumoExpandidoEmCongresso:
                                iessimoItem = ResumoExpandidoEmCongresso(self.idMembro, self.partesDoItem, self.doi,
                                                                         self.relevante)
                                self.listaResumoExpandidoEmCongresso.append(iessimoItem)
                                self.doi = ''
                                self.relevante = 0

                            if self.achouResumoEmCongresso:
                                iessimoItem = ResumoEmCongresso(self.idMembro, self.partesDoItem, self.doi,
                                                                self.relevante)
                                self.listaResumoEmCongresso.append(iessimoItem)
                                self.doi = ''
                                self.relevante = 0








        if tag=='span':
            if self.spanInformacaoArtigo:
                self.spanInformacaoArtigo = 0


    # ------------------------------------------------------------------------ #
    def handle_data(self, dado):
        if not self.spanInformacaoArtigo:
            self.item = self.item + htmlentitydecode(dado)

        dado = stripBlanks(dado)

        if self.salvarAtualizacaoCV:
            data = re.findall(u'Ultima atualizacao do curriculo em (\d{2}/\d{2}/\d{4})', dado)
            if len(data)>0:
                self.atualizacaoCV = stripBlanks(data[0])
                self.salvarAtualizacaoCV = 0

        if self.procurarCabecalho:
            if u'Identificação'==dado:
                self.achouIdentificacao = 1
            if u'Endereço'==dado:
                self.achouEndereco = 1
            if u'Formação acadêmica/titulação'==dado:
                self.achouFormacaoAcademica = 1
            if u'Atuação Profissional'==dado:
                self.achouAtuacaoProfissional = 1
            if u'Membro de corpo editorial'==dado:
                self.achouMembroDeCorpoEditorial = 1
            if u'Revisor de periódico'==dado:
                self.achouRevisorDePeriodico = 1
            if u'Áreas de atuação'==dado:
                self.achouAreaDeAtuacao = 1
            if u'Idiomas'==dado:
                self.achouIdioma = 1
            if u'Produções'==dado:  # !---
                self.achouProducoes = 1

            if u'Bancas'==dado:
                self.achouBancas = 1


            if u'Outras informações relevantes'==dado:
                self.achouOutrasInformacoesRelevantes = 1
            self.umaUnidade = 0
        if self.achouIdentificacao:
            if u'Nome em citações bibliográficas'==dado:
                self.achouNomeEmCitacoes = 1
            if u'Sexo'==dado:
                self.achouSexo = 1

        if self.achouEndereco:
            if u'Endereço Profissional'==dado:
                self.achouEnderecoProfissional = 1



        if self.achouProducoes:
            if u'Produção bibliográfica'==dado:
                self.achouProducaoEmCTA = 1
            if u'Produção técnica'==dado:
                self.achouProducaoEmCTA = 0


            if u'Demais trabalhos'==dado:
                self.salvarItem = 0
                self.achouProducaoEmCTA = 0


            if self.achouProducaoEmCTA:
                if u'Artigos completos publicados em periódicos'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 1
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Livros publicados/organizados ou edições'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 1
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Capítulos de livros publicados'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 1
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Textos em jornais de notícias/revistas'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 1
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Trabalhos completos publicados em anais de congressos'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 1
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Resumos expandidos publicados em anais de congressos'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 1
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Resumos publicados em anais de congressos' in dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 1
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Artigos aceitos para publicação'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 1
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Apresentações de Trabalho'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 1
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u'Outras produções bibliográficas'==dado:
                #if u'Demais tipos de produção bibliográfica'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 1




        if self.achouBancas:
            if u'Participação em bancas de trabalhos de conclusão'==dado:
                self.salvarItem = 0







        if self.achouOutrasInformacoesRelevantes:
            self.salvarItem = 0

        if self.recuperarIdentificador16 and self.identificador16 == '':
          id = re.findall(u'http://lattes.cnpq.br/(\d{16})', dado)
          if len(id) > 0:
            self.identificador16 = id[0]




# ---------------------------------------------------------------------------- #
def stripBlanks(s):
    return re.sub('\s+', ' ', s).strip()

def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint),
        lambda m: unichr(name2codepoint[m.group(1)]), s)
