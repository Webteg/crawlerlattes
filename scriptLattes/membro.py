#!/usr/bin/python
#  encoding: utf-8
#
#
#  scriptLattes
#  Copyright http://scriptlattes.sourceforge.net/
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

import sets
import time
import os
# from htmlentitydefs import name2codepoint
import pandas
from lxml import etree
from baixaLattes import baixaCVLattes

from parserLattes import *
from parserLattesXML import *



class Membro:
    idLattes = None  # ID Lattes
    idMembro = None
    rotulo = ''

    nomeInicial = ''
    nomeCompleto = ''
    sexo = ''
    nomeEmCitacoesBibliograficas = ''
    periodo = ''
    listaPeriodo = []
    bolsaProdutividade = ''
    enderecoProfissional = ''
    enderecoProfissionalLat = ''
    enderecoProfissionalLon = ''

    identificador10 = ''
    url = ''
    atualizacaoCV = ''
    foto = ''
    textoResumo = ''
    ### xml = None


    itemsDesdeOAno = ''  # periodo global
    itemsAteOAno = ''  # periodo global
    diretorioCache = ''  # diretorio de armazento de CVs (útil para extensas listas de CVs)

    listaFormacaoAcademica = []
    listaAreaDeAtuacao = []
    listaIdioma = []


    listaIDLattesColaboradores = []
    listaIDLattesColaboradoresUnica = []

    # Produção bibliográfica
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



    # Qualis
    # tabelaQualisDosAnos = [{}]
    # tabelaQualisDosTipos = {}
    # tabelaQualisDasCategorias = [{}]

    rotuloCorFG = ''
    rotuloCorBG = ''

    tabela_qualis = pandas.DataFrame(columns=['ano', 'area', 'estrato', 'freq'])

    nomePrimeiraGrandeArea = ''
    nomePrimeiraArea       = ''
    instituicao            = ''



    ###def __init__(self, idMembro, identificador, nome, periodo, rotulo, itemsDesdeOAno, itemsAteOAno, xml=''):

    def __init__(self, idMembro, identificador, nome, periodo, rotulo, itemsDesdeOAno, itemsAteOAno, diretorioCache):
        self.idMembro = idMembro
        self.idLattes = identificador
        self.nomeInicial = nome
        self.nomeCompleto = nome.split(";")[0].strip().decode('utf8', 'replace')
        self.periodo = periodo
        self.rotulo = rotulo
        self.rotuloCorFG = '#000000'
        self.rotuloCorBG = '#FFFFFF'


        p = re.compile('[a-zA-Z]+')

        if p.match(identificador):
            self.url = 'http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=' + identificador
        else:
            self.url = 'http://lattes.cnpq.br/' + identificador

        self.itemsDesdeOAno = itemsDesdeOAno
        self.itemsAteOAno = itemsAteOAno
        self.criarListaDePeriodos(self.periodo)
        self.diretorioCache = diretorioCache

    def criarListaDePeriodos(self, periodoDoMembro):
        self.listaPeriodo = []
        periodoDoMembro = re.sub('\s+', '', periodoDoMembro)

        if not periodoDoMembro:  # se nao especificado o periodo, entao aceitamos todos os items do CV Lattes
            self.listaPeriodo = [[0, 10000]]
        else:
            lista = periodoDoMembro.split("&")
            for periodo in lista:
                ano1, _, ano2 = periodo.partition("-")

                if ano1.lower() == 'hoje':
                    ano1 = str(datetime.datetime.now().year)
                if ano2.lower() == 'hoje' or ano2 == '':
                    ano2 = str(datetime.datetime.now().year)

                if ano1.isdigit() and ano2.isdigit():
                    self.listaPeriodo.append([int(ano1), int(ano2)])
                else:
                    print(
                    "\n[AVISO IMPORTANTE] Periodo nao válido: {}. (periodo desconsiderado na lista)".format(periodo))
                    print("[AVISO IMPORTANTE] CV Lattes: {}. Membro: {}\n".format(self.idLattes,
                                                                                  self.nomeInicial.encode('utf8')))


    def carregarDadosCVLattes(self):
        cvPath = self.diretorioCache + '/' + self.idLattes

        if 'xml' in cvPath:
            arquivoX = open(cvPath)
            cvLattesXML = arquivoX.read()
            arquivoX.close()

            extended_chars = u''.join(unichr(c) for c in xrange(127, 65536, 1))  # srange(r"[\0x80-\0x7FF]")
            special_chars = ' -'''
            cvLattesXML = cvLattesXML.decode('iso-8859-1', 'replace') + extended_chars + special_chars
            parser = ParserLattesXML(self.idMembro, cvLattesXML)

            self.idLattes = parser.idLattes
            self.url = parser.url
            print "(*) Utilizando CV armazenado no cache: " + cvPath

        elif '0000000000000000' == self.idLattes:
            # se o codigo for '0000000000000000' então serao considerados dados de pessoa estrangeira - sem Lattes.
            # sera procurada a coautoria endogena com os outros membro.
            # para isso é necessario indicar o nome abreviado no arquivo .list
            return

        else:
            if os.path.exists(cvPath):
                arquivoH = open(cvPath)
                cvLattesHTML = arquivoH.read()
                if self.idMembro!='':
                    print "(*) Utilizando CV armazenado no cache: "+cvPath
            else:
                cvLattesHTML = baixaCVLattes(self.idLattes)
                if not self.diretorioCache=='':
                    file = open(cvPath, 'w')
                    file.write(cvLattesHTML)
                    file.close()
                    print " (*) O CV está sendo armazenado no Cache"

            extended_chars = u''.join(unichr(c) for c in xrange(127, 65536, 1))  # srange(r"[\0x80-\0x7FF]")
            special_chars = ' -'''
            #cvLattesHTML  = cvLattesHTML.decode('ascii','replace')+extended_chars+special_chars                                          # Wed Jul 25 16:47:39 BRT 2012
            cvLattesHTML = cvLattesHTML.decode('iso-8859-1', 'replace') + extended_chars + special_chars
            parser = ParserLattes(self.idMembro, cvLattesHTML)

            p = re.compile('[a-zA-Z]+')
            if p.match(self.idLattes):
                self.identificador10 = self.idLattes
                self.idLattes = parser.identificador16
                self.url = 'http://lattes.cnpq.br/' + self.idLattes

        # -----------------------------------------------------------------------------------------
        # Obtemos todos os dados do CV Lattes
        self.nomeCompleto = parser.nomeCompleto
        self.bolsaProdutividade = parser.bolsaProdutividade
        self.enderecoProfissional = parser.enderecoProfissional
        self.sexo = parser.sexo
        self.nomeEmCitacoesBibliograficas = parser.nomeEmCitacoesBibliograficas
        self.atualizacaoCV = parser.atualizacaoCV
        self.textoResumo = parser.textoResumo
        self.foto = parser.foto

        self.listaIDLattesColaboradores = parser.listaIDLattesColaboradores
        self.listaFormacaoAcademica = parser.listaFormacaoAcademica
        self.listaAreaDeAtuacao = parser.listaAreaDeAtuacao
        self.listaIdioma = parser.listaIdioma
        self.listaIDLattesColaboradoresUnica = sets.Set(self.listaIDLattesColaboradores)

        # Produção bibliográfica
        self.listaArtigoEmPeriodico = parser.listaArtigoEmPeriodico
        self.listaLivroPublicado = parser.listaLivroPublicado
        self.listaCapituloDeLivroPublicado = parser.listaCapituloDeLivroPublicado
        self.listaTextoEmJornalDeNoticia = parser.listaTextoEmJornalDeNoticia
        self.listaTrabalhoCompletoEmCongresso = parser.listaTrabalhoCompletoEmCongresso
        self.listaResumoExpandidoEmCongresso = parser.listaResumoExpandidoEmCongresso
        self.listaResumoEmCongresso = parser.listaResumoEmCongresso
        self.listaArtigoAceito = parser.listaArtigoAceito
        self.listaApresentacaoDeTrabalho = parser.listaApresentacaoDeTrabalho
        self.listaOutroTipoDeProducaoBibliografica = parser.listaOutroTipoDeProducaoBibliografica




        # Eventos
        self.listaParticipacaoEmEvento = parser.listaParticipacaoEmEvento
        self.listaOrganizacaoDeEvento = parser.listaOrganizacaoDeEvento

        # -----------------------------------------------------------------------------------------
        nomePrimeiraGrandeArea = ""
        nomePrimeiraArea = ""

        if len(self.listaAreaDeAtuacao)>0:
            descricao = self.listaAreaDeAtuacao[0].descricao
            partes = descricao.split('/')
            nomePrimeiraGrandeArea = partes[0]
            nomePrimeiraGrandeArea = nomePrimeiraGrandeArea.replace("Grande área:".decode('utf-8'), '').strip()

            if len(partes)>1:
                partes = partes[1].split(":")
                partes = partes[1].strip()
                nomePrimeiraArea = partes
                nomePrimeiraArea = nomePrimeiraArea.strip(".")
                nomePrimeiraArea = nomePrimeiraArea.replace("Especialidade", "")
        else:
            nomePrimeiraGrandeArea = "[sem-grandeArea]"
            nomePrimeiraArea = "[sem-area]"


        self.nomePrimeiraGrandeArea = nomePrimeiraGrandeArea
        self.nomePrimeiraArea = nomePrimeiraArea

        if len(self.enderecoProfissional)>0:
            instituicao = self.enderecoProfissional.split(".")[0]
            self.instituicao = instituicao.replace("'","")


    def filtrarItemsPorPeriodo(self):
        self.listaArtigoEmPeriodico = self.filtrarItems(self.listaArtigoEmPeriodico)
        self.listaLivroPublicado = self.filtrarItems(self.listaLivroPublicado)
        self.listaCapituloDeLivroPublicado = self.filtrarItems(self.listaCapituloDeLivroPublicado)
        self.listaTextoEmJornalDeNoticia = self.filtrarItems(self.listaTextoEmJornalDeNoticia)
        self.listaTrabalhoCompletoEmCongresso = self.filtrarItems(self.listaTrabalhoCompletoEmCongresso)
        self.listaResumoExpandidoEmCongresso = self.filtrarItems(self.listaResumoExpandidoEmCongresso)
        self.listaResumoEmCongresso = self.filtrarItems(self.listaResumoEmCongresso)
        self.listaArtigoAceito = self.filtrarItems(self.listaArtigoAceito)
        self.listaApresentacaoDeTrabalho = self.filtrarItems(self.listaApresentacaoDeTrabalho)
        self.listaOutroTipoDeProducaoBibliografica = self.filtrarItems(self.listaOutroTipoDeProducaoBibliografica)

        self.listaParticipacaoEmEvento = self.filtrarItems(self.listaParticipacaoEmEvento)
        self.listaOrganizacaoDeEvento = self.filtrarItems(self.listaOrganizacaoDeEvento)

    def estaDentroDoPeriodo(self, objeto):
        if not objeto.ano.isdigit():  # se nao for identificado o ano sempre o mostramos na lista
            objeto.ano = 0
            return 1
        else:
            objeto.ano = int(objeto.ano)
            if self.itemsDesdeOAno > objeto.ano or objeto.ano > self.itemsAteOAno:
                return 0
            else:
                retorno = 0
                for per in self.listaPeriodo:
                    if per[0] <= objeto.ano and objeto.ano <= per[1]:
                        retorno = 1
                        break
                return retorno

    def filtrarItems(self, lista):
        return filter(self.estaDentroDoPeriodo, lista)




    def ris(self):
        s = ''
        s += '\nTY  - MEMBRO'
        s += '\nNOME  - ' + self.nomeCompleto
        #s+= '\nSEXO  - '+self.sexo
        s += '\nCITA  - ' + self.nomeEmCitacoesBibliograficas
        s += '\nBOLS  - ' + self.bolsaProdutividade
        s += '\nENDE  - ' + self.enderecoProfissional
        s += '\nURLC  - ' + self.url
        s += '\nDATA  - ' + self.atualizacaoCV
        s += '\nRESU  - ' + self.textoResumo

        for i in range(0, len(self.listaFormacaoAcademica)):
            formacao = self.listaFormacaoAcademica[i]
            s += '\nFO' + str(i + 1) + 'a  - ' + formacao.anoInicio
            s += '\nFO' + str(i + 1) + 'b  - ' + formacao.anoConclusao
            s += '\nFO' + str(i + 1) + 'c  - ' + formacao.tipo
            s += '\nFO' + str(i + 1) + 'd  - ' + formacao.nomeInstituicao
            s += '\nFO' + str(i + 1) + 'e  - ' + formacao.descricao

        for i in range(0, len(self.listaAreaDeAtuacao)):
            area = self.listaAreaDeAtuacao[i]
            s += '\nARE' + str(i + 1) + '  - ' + area.descricao

        for i in range(0, len(self.listaIdioma)):
            idioma = self.listaIdioma[i]
            s += '\nID' + str(i + 1) + 'a  - ' + idioma.nome
            s += '\nID' + str(i + 1) + 'b  - ' + idioma.proficiencia

        return s


    def __str__(self):
        verbose = 0

        s = "+ ID-MEMBRO   : " + str(self.idMembro) + "\n"
        s += "+ ROTULO      : " + self.rotulo + "\n"
        #s += "+ ALIAS       : " + self.nomeInicial.encode('utf8','replace') + "\n"
        s += "+ NOME REAL   : " + self.nomeCompleto.encode('utf8', 'replace') + "\n"
        #s += "+ SEXO        : " + self.sexo.encode('utf8','replace') + "\n"
        #s += "+ NOME Cits.  : " + self.nomeEmCitacoesBibliograficas.encode('utf8','replace') + "\n"
        #s += "+ PERIODO     : " + self.periodo.encode('utf8','replace') + "\n"
        #s += "+ BOLSA Prod. : " + self.bolsaProdutividade.encode('utf8','replace') + "\n"
        #s += "+ ENDERECO    : " + self.enderecoProfissional.encode('utf8','replace') +"\n"
        #s += "+ URL         : " + self.url.encode('utf8','replace') +"\n"
        #s += "+ ATUALIZACAO : " + self.atualizacaoCV.encode('utf8','replace') +"\n"
        #s += "+ FOTO        : " + self.foto.encode('utf8','replace') +"\n"
        #s += "+ RESUMO      : " + self.textoResumo.encode('utf8','replace') + "\n"
        #s += "+ COLABORADs. : " + str(len(self.listaIDLattesColaboradoresUnica))

        if verbose:
            s += "\n[COLABORADORES]"
            for idColaborador in self.listaIDLattesColaboradoresUnica:
                s += "\n+ " + idColaborador.encode('utf8', 'replace')

        else:
            s += "\n- Numero de colaboradores (identificado)      : " + str(len(self.listaIDLattesColaboradoresUnica))
            s += "\n- Artigos completos publicados em periódicos  : " + str(len(self.listaArtigoEmPeriodico))
            s += "\n- Livros publicados/organizados ou edições    : " + str(len(self.listaLivroPublicado))
            s += "\n- Capítulos de livros publicados              : " + str(len(self.listaCapituloDeLivroPublicado))
            s += "\n- Textos em jornais de notícias/revistas      : " + str(len(self.listaTextoEmJornalDeNoticia))
            s += "\n- Trabalhos completos publicados em congressos: " + str(len(self.listaTrabalhoCompletoEmCongresso))
            s += "\n- Resumos expandidos publicados em congressos : " + str(len(self.listaResumoExpandidoEmCongresso))
            s += "\n- Resumos publicados em anais de congressos   : " + str(len(self.listaResumoEmCongresso))
            s += "\n- Artigos aceitos para publicação             : " + str(len(self.listaArtigoAceito))
            s += "\n- Apresentações de Trabalho                   : " + str(len(self.listaApresentacaoDeTrabalho))
            s += "\n- Demais tipos de produção bibliográfica      : " + str(len(self.listaOutroTipoDeProducaoBibliografica))

            s += "\n\n"
        return s



# ---------------------------------------------------------------------------- #
# http://wiki.python.org/moin/EscapingHtml
def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint),
                  lambda m: unichr(name2codepoint[m.group(1)]), s)
