#!/usr/bin/python
# encoding: utf-8
# filename: geradorDePaginasWeb
#
#  scriptLattes V8
#  Copyright 2005-2013: Jesús P. Mena-Chalco e Roberto M. Cesar-Jr.
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
import datetime

from grupo import *


class GeradorDeXML:
    grupo = None
    dir = None
    version = None
    extensaoPagina = None
    arquivoRis = None
    membros = None
    listaErroXml = list()

    def __init__(self, gr):
        self.grupo = gr
        self.membros = gr.listaDeMembros
        self.dir = self.grupo.obterParametro('global-diretorio_de_saida')

    def gerarXmlParaGrupo(self):
        print '\n\n[GERANDO XML PARA CADA UM DOS CVs LATTES]'
        xmlTemp = ''  # variavel importante para continuar a varredura dos membros caso ocorra erros

        xml = ''
        xml += "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
        xml += '<curriculo_lattes data_processamento="' + self.getDataProcessamento() + '">\n'
        for registro in self.membros:
            print "- ID Lattes: [" + registro.idLattes + "]"
            try:
                xmlTemp = '  <pesquisador id="' + registro.idLattes + '">\n'

                xmlTemp += self.getDadosIdentificacao(registro)
                xmlTemp += self.getIdiomas(registro)
                xmlTemp += self.getDadosEndereco(registro)
                xmlTemp += self.getFormacaoAcademica(registro)
                xmlTemp += self.getAreaDeAtuacao(registro)
                xmlTemp += self.getListaColaborares(registro)
                xmlTemp += self.getListaArtigosEmPeriodicos(registro)
                xmlTemp += self.getListaLivroPublicado(registro)
                xmlTemp += self.getListaCapituloDeLivroPublicado(registro)
                xmlTemp += self.getListaTextoEmJornalDeNoticia(registro)
                xmlTemp += self.getListaTrabalhoCompletoEmCongresso(registro)
                xmlTemp += self.getListaResumoExpandidoEmCongresso(registro)
                xmlTemp += self.getListaResumoEmCongresso(registro)
                xmlTemp += self.getListaArtigoAceito(registro)
                xmlTemp += self.getListaApresentacaoDeTrabalho(registro)
                xmlTemp += self.getListaOutroTipoDeProducaoBibliografica(registro)

                xmlTemp += self.getListaParticipacaoEmEvento(registro)
                xmlTemp += self.getListaOrganizacaoDeEvento(registro)

                xmlTemp += '  </pesquisador>\n'
            except:
                # adicionar ids para a lista de erros
                self.listaErroXml.append(registro.idLattes)
                continue

            xml += xmlTemp

        xml += '</curriculo_lattes>\n'
        self.salvarXML("database.xml", xml)

        # print "[Liberando memoria usada na geracao do XML]"
        xml = ""
        xmlTemp = ""

    def getDataProcessamento(self):
        agora = datetime.datetime.now()
        dia = '0' + str(agora.day)
        mes = '0' + str(agora.month)
        ano = str(agora.year)
        hora = '0' + str(agora.hour)
        minuto = '0' + str(agora.minute)
        segundo = '0' + str(agora.second)

        dia = dia[-2:]
        mes = mes[-2:]
        hora = hora[-2:]
        minuto = minuto[-2:]
        segundo = segundo[-2:]
        data = dia + "/" + mes + "/" + ano + " " + hora + ":" + minuto + ":" + segundo

        return data


    def getListaOrganizacaoDeEvento(self, registro):
        xmlTemp = ''
        if registro.listaOrganizacaoDeEvento:
            xmlTemp += '    <organizacao_evento>\n'
            for evento in registro.listaOrganizacaoDeEvento:
                xmlTemp += '        <evento>\n'
                xmlTemp += '          <titulo>' + evento.nomeDoEvento + '</titulo>\n'
                xmlTemp += '          <natureza>' + evento.natureza + '</natureza>\n'
                xmlTemp += '          <ano>' + str(evento.ano) + '</ano>\n'
                xmlTemp += '        </evento>\n'
            xmlTemp += '    </organizacao_evento>\n'
        return xmlTemp

    def getListaParticipacaoEmEvento(self, registro):
        xmlTemp = ''
        if registro.listaParticipacaoEmEvento:
            xmlTemp += '    <participacao_evento>\n'
            for evento in registro.listaParticipacaoEmEvento:
                xmlTemp += '        <evento>\n'
                xmlTemp += '          <titulo>' + evento.item + '</titulo>\n'
                xmlTemp += '          <ano>' + str(evento.ano) + '</ano>\n'
                xmlTemp += '        </evento>\n'
            xmlTemp += '    </participacao_evento>\n'
        return xmlTemp



    def getListaOutroTipoDeProducaoBibliografica(self, registro):
        xmlTemp = ''
        if registro.listaOutroTipoDeProducaoBibliografica:
            xmlTemp += '    <producao_bibliografica>\n'
            for producao in registro.listaOutroTipoDeProducaoBibliografica:
                xmlTemp += '        <producao>\n'
                xmlTemp += '          <titulo>' + producao.titulo + '</titulo>\n'
                xmlTemp += '          <autores>' + producao.autores + '</autores>\n'
                xmlTemp += '          <ano>' + str(producao.ano) + '</ano>\n'
                xmlTemp += '          <natureza>' + producao.natureza + '</natureza>\n'
                xmlTemp += '        </producao>\n'
            xmlTemp += '    </producao_bibliografica>\n'
        return xmlTemp


    def getListaApresentacaoDeTrabalho(self, registro):
        xmlTemp = ''
        if registro.listaApresentacaoDeTrabalho:
            xmlTemp += '    <apresentacao_trabalho>\n'
            for apresentacao in registro.listaApresentacaoDeTrabalho:
                xmlTemp += '        <trabalho_apresentado>\n'
                xmlTemp += '          <titulo>' + apresentacao.titulo + '</titulo>\n'
                xmlTemp += '          <autores>' + apresentacao.autores + '</autores>\n'
                xmlTemp += '          <ano>' + str(apresentacao.ano) + '</ano>\n'
                xmlTemp += '          <natureza>' + apresentacao.natureza + '</natureza>\n'
                xmlTemp += '        </trabalho_apresentado>\n'
            xmlTemp += '    </apresentacao_trabalho>\n'
        return xmlTemp


    def getListaArtigoAceito(self, registro):
        xmlTemp = ''
        if registro.listaArtigoAceito:
            xmlTemp += '    <artigos_em_revista>\n'
            for artigo in registro.listaArtigoAceito:
                xmlTemp += '        <artigo_revista>\n'
                xmlTemp += '          <doi>' + artigo.doi + '</doi>\n'
                xmlTemp += '          <autores>' + artigo.autores + '</autores>\n'
                xmlTemp += '          <titulo>' + artigo.titulo + '</titulo>\n'
                xmlTemp += '          <revista>' + artigo.revista + '</revista>\n'
                xmlTemp += '          <ano>' + str(artigo.ano) + '</ano>\n'
                xmlTemp += '          <volume>' + artigo.volume + '</volume>\n'
                xmlTemp += '          <paginas>' + artigo.paginas + '</paginas>\n'
                xmlTemp += '          <numero>' + artigo.numero + '</numero>\n'
                xmlTemp += '        </artigo_revista>\n'
            xmlTemp += '    </artigos_em_revista>\n'

        return xmlTemp

    def getListaResumoEmCongresso(self, registro):
        xmlTemp = ''
        if registro.listaResumoEmCongresso:
            xmlTemp += '    <resumo_congresso>\n'
            for resumo in registro.listaResumoEmCongresso:
                xmlTemp += '        <resumo>\n'
                xmlTemp += '          <doi>' + resumo.doi + '</doi>\n'
                xmlTemp += '          <autores>' + resumo.autores + '</autores>\n'
                xmlTemp += '          <titulo>' + resumo.titulo + '</titulo>\n'
                xmlTemp += '          <nome_evento>' + resumo.nomeDoEvento + '</nome_evento>\n'
                xmlTemp += '          <ano>' + str(resumo.ano) + '</ano>\n'
                xmlTemp += '          <volume>' + resumo.volume + '</volume>\n'
                xmlTemp += '          <paginas>' + resumo.paginas + '</paginas>\n'
                xmlTemp += '          <numero>' + resumo.numero + '</numero>\n'
                xmlTemp += '        </resumo>\n'
            xmlTemp += '    </resumo_congresso>\n'
        return xmlTemp

    def getListaResumoExpandidoEmCongresso(self, registro):
        xmlTemp = ''
        if registro.listaResumoExpandidoEmCongresso:
            xmlTemp += '    <resumo_expandido_congresso>\n'
            for resumo in registro.listaResumoExpandidoEmCongresso:
                xmlTemp += '        <resumo_expandido>\n'
                xmlTemp += '          <doi>' + resumo.doi + '</doi>\n'
                xmlTemp += '          <autores>' + resumo.autores + '</autores>\n'
                xmlTemp += '          <titulo>' + resumo.titulo + '</titulo>\n'
                xmlTemp += '          <nome_evento>' + resumo.nomeDoEvento + '</nome_evento>\n'
                xmlTemp += '          <ano>' + str(resumo.ano) + '</ano>\n'
                xmlTemp += '          <volume>' + resumo.volume + '</volume>\n'
                xmlTemp += '          <paginas>' + resumo.paginas + '</paginas>\n'
                xmlTemp += '        </resumo_expandido>\n'
            xmlTemp += '    </resumo_expandido_congresso>\n'
        return xmlTemp


    def getListaTrabalhoCompletoEmCongresso(self, registro):
        xmlTemp = ''
        if registro.listaTrabalhoCompletoEmCongresso:
            xmlTemp += '    <trabalho_completo_congresso>\n'
            for trabalho_completo in registro.listaTrabalhoCompletoEmCongresso:
                xmlTemp += '        <trabalho_completo>\n'
                xmlTemp += '          <doi>' + trabalho_completo.doi + '</doi>\n'
                xmlTemp += '          <autores>' + trabalho_completo.autores + '</autores>\n'
                xmlTemp += '          <titulo>' + trabalho_completo.titulo + '</titulo>\n'
                xmlTemp += '          <nome_evento>' + trabalho_completo.nomeDoEvento + '</nome_evento>\n'
                xmlTemp += '          <ano>' + str(trabalho_completo.ano) + '</ano>\n'
                xmlTemp += '          <volume>' + trabalho_completo.volume + '</volume>\n'
                xmlTemp += '          <paginas>' + trabalho_completo.paginas + '</paginas>\n'
                xmlTemp += '        </trabalho_completo>\n'
            xmlTemp += '    </trabalho_completo_congresso>\n'
        return xmlTemp

    def getListaTextoEmJornalDeNoticia(self, registro):
        xmlTemp = ''
        if registro.listaTextoEmJornalDeNoticia:
            xmlTemp += '    <texto_em_jornal>\n'
            for texto_jornal in registro.listaTextoEmJornalDeNoticia:
                xmlTemp += '        <texto>\n'
                xmlTemp += '          <ano>' + str(texto_jornal.ano) + '</ano>\n'
                xmlTemp += '          <autores>' + texto_jornal.autores + '</autores>\n'
                xmlTemp += '          <titulo>' + texto_jornal.titulo + '</titulo>\n'
                xmlTemp += '          <nome_jornal>' + texto_jornal.nomeJornal + '</nome_jornal>\n'
                xmlTemp += '          <data>' + texto_jornal.data + '</data>\n'
                xmlTemp += '          <volume>' + texto_jornal.volume + '</volume>\n'
                xmlTemp += '          <paginas>' + texto_jornal.paginas + '</paginas>\n'
                xmlTemp += '        </texto>\n'
            xmlTemp += '    </texto_em_jornal>\n'
        return xmlTemp

    def getListaCapituloDeLivroPublicado(self, registro):
        xmlTemp = ''
        if registro.listaCapituloDeLivroPublicado:
            xmlTemp += '    <capitulos_livros>\n'
            for capitulo in registro.listaCapituloDeLivroPublicado:
                xmlTemp += '        <capitulo>\n'
                xmlTemp += '          <livro>' + capitulo.livro + '</livro>\n'
                xmlTemp += '          <titulo>' + capitulo.titulo + '</titulo>\n'
                xmlTemp += '          <autores>' + capitulo.autores + '</autores>\n'
                xmlTemp += '          <edicao>' + capitulo.edicao + '</edicao>\n'
                xmlTemp += '          <editora>' + capitulo.editora + '</editora>\n'
                xmlTemp += '          <volume>' + capitulo.volume + '</volume>\n'
                xmlTemp += '          <paginas>' + capitulo.paginas + '</paginas>\n'
                xmlTemp += '          <ano>' + str(capitulo.ano) + '</ano>\n'
                xmlTemp += '        </capitulo>\n'
            xmlTemp += '    </capitulos_livros>\n'
        return xmlTemp


    def getListaLivroPublicado(self, registro):
        xmlTemp = ''
        if registro.listaLivroPublicado:
            xmlTemp += '    <livros_publicados>\n'
            for livro_publicado in registro.listaLivroPublicado:
                xmlTemp += '        <livro>\n'
                xmlTemp += '          <autores>' + livro_publicado.autores + '</autores>\n'
                xmlTemp += '          <titulo>' + livro_publicado.titulo + '</titulo>\n'
                xmlTemp += '          <edicao>' + livro_publicado.edicao + '</edicao>\n'
                xmlTemp += '          <volume>' + livro_publicado.volume + '</volume>\n'
                xmlTemp += '          <paginas>' + livro_publicado.paginas + '</paginas>\n'
                xmlTemp += '          <ano>' + str(livro_publicado.ano) + '</ano>\n'
                xmlTemp += '        </livro>\n'
            xmlTemp += '    </livros_publicados>\n'
        return xmlTemp


    def getListaArtigosEmPeriodicos(self, registro):
        xmlTemp = ''
        if registro.listaArtigoEmPeriodico:
            xmlTemp += '    <artigos_em_periodicos>\n'
            for artigos_periodicos in registro.listaArtigoEmPeriodico:
                xmlTemp += '        <artigo>\n'
                xmlTemp += '          <doi>' + artigos_periodicos.doi + '</doi>\n'
                xmlTemp += '          <titulo>' + artigos_periodicos.titulo + '</titulo>\n'
                xmlTemp += '          <autores>' + artigos_periodicos.autores + '</autores>\n'
                xmlTemp += '          <revista>' + artigos_periodicos.revista + '</revista>\n'
                xmlTemp += '          <volume>' + artigos_periodicos.revista + '</volume>\n'
                xmlTemp += '          <paginas>' + artigos_periodicos.paginas + '</paginas>\n'
                xmlTemp += '          <numero>' + artigos_periodicos.numero + '</numero>\n'
                xmlTemp += '          <ano>' + str(artigos_periodicos.ano) + '</ano>\n'
                xmlTemp += '        </artigo>\n'
            xmlTemp += '    </artigos_em_periodicos>\n'
        return xmlTemp

    def getListaColaborares(self, registro):
        xmlTemp = ''
        if registro.listaIDLattesColaboradoresUnica:
            xmlTemp += '    <colaboradores>\n'
            for idColaborador in registro.listaIDLattesColaboradoresUnica:
                xmlTemp += '        <id_lattes_colaborador>' + idColaborador + '</id_lattes_colaborador>\n'
            xmlTemp += '    </colaboradores>\n'
        return xmlTemp





    def getDadosIdentificacao(self, registro):
        xmlTemp = ''
        xmlTemp += '    <identificacao>\n'
        xmlTemp += '      <identificador10>' + registro.identificador10 + '</identificador10>\n'
        xmlTemp += '      <nome_inicial>' + registro.nomeInicial.decode('utf8', 'ignore') + '</nome_inicial>\n'
        xmlTemp += '      <nome_completo>' + registro.nomeCompleto + '</nome_completo>\n'
        xmlTemp += '      <nome_citacao_bibliografica>' + registro.nomeEmCitacoesBibliograficas + '</nome_citacao_bibliografica>\n'
        xmlTemp += '      <sexo>' + registro.sexo.encode('utf8', 'replace') + '</sexo>\n'
        xmlTemp += '    </identificacao>\n'
        return xmlTemp

    def getDadosEndereco(self, registro):
        xmlTemp = ''
        xmlTemp += '    <endereco>\n'
        xmlTemp += '      <endereco_profissional>' + registro.enderecoProfissional + '</endereco_profissional>\n'
        xmlTemp += '      <endereco_profissional_lat>' + registro.enderecoProfissionalLat + '</endereco_profissional_lat>\n'
        xmlTemp += '      <endereco_profissional_long>' + registro.enderecoProfissionalLon + '</endereco_profissional_long>\n'
        xmlTemp += '    </endereco>\n'
        return xmlTemp

    def getFormacaoAcademica(self, registro):
        xmlTemp = ''
        if registro.listaFormacaoAcademica:
            xmlTemp += '    <formacao_academica>\n'
            for formacao in registro.listaFormacaoAcademica:
                xmlTemp += '        <formacao>\n'
                xmlTemp += '          <ano_inicio>' + formacao.anoInicio + '</ano_inicio>\n'
                xmlTemp += '          <ano_conclusao>' + formacao.anoConclusao + '</ano_conclusao>\n'
                xmlTemp += '          <tipo>' + formacao.tipo + '</tipo>\n'
                xmlTemp += '          <nome_instituicao>' + formacao.nomeInstituicao + '</nome_instituicao>\n'
                xmlTemp += '          <descricao>' + formacao.descricao + '</descricao>\n'
                xmlTemp += '        </formacao>\n'
            xmlTemp += '    </formacao_academica>\n'
        return xmlTemp




    def getAreaDeAtuacao(self, registro):
        xmlTemp = ''
        if registro.listaAreaDeAtuacao:
            xmlTemp += '    <area_atuacao>\n'
            for atuacao in registro.listaAreaDeAtuacao:
                xmlTemp += '          <descricao>' + atuacao.descricao + '</descricao>\n'
            xmlTemp += '    </area_atuacao>\n'
        return xmlTemp


    def getIdiomas(self, registro):
        xmlTemp = ''
        if registro.listaIdioma:
            xmlTemp += '    <idiomas>\n'
            for idioma in registro.listaIdioma:
                xmlTemp += '      <idioma>\n'
                xmlTemp += '          <nome>' + idioma.nome + '</nome>\n'
                xmlTemp += '          <proficiencia>' + idioma.proficiencia + '</proficiencia>\n'
                xmlTemp += '      </idioma>\n'
            xmlTemp += '    </idiomas>\n'
        return xmlTemp


    def salvarXML(self, nome, conteudo):
        prefix = self.grupo.obterParametro('global-prefixo') + '-' if not self.grupo.obterParametro(
            'global-prefixo') == '' else ''
        file = open(self.dir + "/" + prefix + nome, 'w')
        file.write(conteudo.encode('utf8'))
        file.close()
