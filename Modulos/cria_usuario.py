import json

#MAXIMO MINIMO IDEAL
class MMI:
    def __init__(self, maximo, minimo, ideal):
        self.maximo = maximo
        self.minimo = minimo
        self.ideal = ideal

#Especifica para coisas com relaçao DIA - MMI
class MMIDiaEspecifico:
    def __init__(self, dia, mmi):
        self.dia = dia #numero, [0..6], representando dia da semana
        self.mmi = mmi

#DADOS PESSOAIS
class Pessoa:
    def __init__(self, nome, sobrenome, idade, periodo, curso):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
        self.periodo = periodo
        self.curso = curso

#REGISTRA MATÉRIA
class Materia:
    def __init__(self, nome, creditos, dificuldade, possibilidades=[]):
        self.nome = nome
        self.creditos = creditos
        self.dificuldade = dificuldade
        self.possibilidades = [PossibilidadesMateria(*poss) for poss in possibilidades]

#MATÉRIA - REGISTRA COMBINAÇÃO HORARIO-PROFESSOR REFERENTE A MATERIA
class PossibilidadesMateria:
    def __init__(self, preferencia, professores=[], horarios=[]):          
        self.preferencia = float(preferencia) if preferencia is not None else None
        self.professores = [Professor(*prof) for prof in professores]
        self.horarios = [Horario(*hor) for hor in horarios]

#MATÉRIA - REGISTRA ESPECIFICIDADES SOBRE PROFESSORES
class Professor:
    def __init__(self, nome, preferencia):
        self.nome = nome
        self.preferencia = float(preferencia) if preferencia is not None else None

#MATÉRIA - REGISTRA ESPECIFICIDADES SOBRE HORÁRIOS
class Horario:
    def __init__(self, inicio, final, preferencia):
        self.inicio = inicio
        self.final = final
        self.preferencia = float(preferencia) if preferencia is not None else None

#REGISTRA PREFERENCIAS DE HORÁRIOS DE CHEGADA-SAIDA 
class PreferenciasDeHorario:
    def __init__(self, chegada_geral_mmi, saida_geral_mmi, chegada_especifica=[], saida_especifica=[]):
        self.chegada_geral_mmi = chegada_geral_mmi  
        self.saida_geral_mmi = saida_geral_mmi      
        self.chegada_especifica = [MMIDiaEspecifico(*chegE) for chegE in chegada_especifica] 
        self.saida_especifica = [MMIDiaEspecifico(*saiE) for saiE in saida_especifica]

#REGISTRA PREFERENCIAS DE CARGA TOTAL (POR DIA)
class Carga:
    def __init__(self, carga_total_geral_mmi, carga_especifica=[] ):
        self.carga_total_geral_mmi = carga_total_geral_mmi    
        self.carga_especifica = [MMIDiaEspecifico(*carE) for carE in carga_especifica] 

#REGISTRA PREFERENCIAS DE CREDITOS (MMI)
class Creditos:
    def __init__(self, creditos_mmi):
        self.creditos_mmi = creditos_mmi    

#REGISTRA PREFERENCIAS DE INTERVALO (lista)
class Intervalos:
    def __init__(self, intervalosEspecificos=[], intervalosDistancia=[]):
        self.intervalosDistancia = [PreferenciasDeIntervaloEspecificos(*iidsE) for iidsE in intervalosDistancia] 
        self.intervalosEspecificos = [PreferenciasDeIntervaloDistancia(*iesE) for iesE in intervalosEspecificos] 
        
#Intervalos - PERSONALIZA LISTA DE INTERVALOS ESPECIFICOS
class PreferenciasDeIntervaloEspecificos:
    def __init__(self, dias, horario_inicio, horario_fim, prioridade):
        self.dias = dias #Se null então todos os dias, do contrario é uma lista contendo 1-7 numeros [0..6]
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.prioridade = prioridade

#Intervalos - PERSONALIZA LISTA DE INTERVALOS POR DISTANCIA
class PreferenciasDeIntervaloDistancia:
    def __init__(self, dias, distancia, repeticoes, prioridade):
        self.dias = dias #Se null então todos os dias, do contrario é uma lista contendo 1-7 numeros [0..6]
        self.distancia = distancia
        self.repeticoes = repeticoes
        self.prioridade = prioridade


#REGISTRA PREFERENCIAS DE DIAS LIVRES (LISTA)
class DiasLivres:
    def __init__(self, dias=[]):
        self.dias = [DiasLivres(*diaE) for diaE in DiasLivresEspecificacao] 

#DiasLivres - ESPECIFICA COM PRIORIDADE DIAS LIVRES
class DiasLivresEspecificacao:
    def __init__(self, dia, prioridade):
        self.dia = dia
        self.prioridade = prioridade 














# Funções Auxiliares
def carregar_configuracoes(arquivo):
    with open(arquivo, 'r') as file:
        dados = json.load(file)
        
        # Carregando dados da pessoa
        pessoa = Pessoa(**dados['pessoa'])
        
        # Carregando matérias e possibilidades associadas
        materias = [Materia(**m) for m in dados['materias']]
        
        # Carregando preferências de horário
        chegada_geral_mmi = MMI(*dados['preferenciasDeHorario']['chegada_geral_mmi'])
        saida_geral_mmi = MMI(*dados['preferenciasDeHorario']['saida_geral_mmi'])
        chegada_especifica = [MMIDiaEspecifico(d['dia'], MMI(*d['mmi'])) for d in dados['preferenciasDeHorario']['chegada_especifica']]
        saida_especifica = [MMIDiaEspecifico(d['dia'], MMI(*d['mmi'])) for d in dados['preferenciasDeHorario']['saida_especifica']]
        preferencias_de_horario = PreferenciasDeHorario(chegada_geral_mmi, saida_geral_mmi, chegada_especifica, saida_especifica)
        
        # Carregando carga total por dia
        carga_total_geral_mmi = MMI(*dados['cargaTotal']['carga_total_geral_mmi'])
        carga_especifica = [MMIDiaEspecifico(d['dia'], MMI(*d['mmi'])) for d in dados['cargaTotal']['carga_especifica']]
        carga_total = Carga(carga_total_geral_mmi, carga_especifica)
        
        # Carregando créditos
        creditos_mmi = MMI(*dados['creditos']['creditos_mmi'])
        creditos = Creditos(creditos_mmi)
        
        # Carregando intervalos
        intervalos_especificos = [PreferenciasDeIntervaloEspecificos(**ie) for ie in dados['intervalos']['intervalosEspecificos']]
        intervalos_distancia = [PreferenciasDeIntervaloDistancia(**id) for id in dados['intervalos']['intervalosDistancia']]
        intervalos = Intervalos(intervalos_especificos, intervalos_distancia)
        
        # Carregando dias livres
        dias_livres = [DiasLivresEspecificacao(**dl) for dl in dados['diasLivres']['dias']]
        dias_livres = DiasLivres(dias_livres)

        return {
            "pessoa": pessoa,
            "materias": materias,
            "preferenciasDeHorario": preferencias_de_horario,
            "cargaTotal": carga_total,
            "creditos": creditos,
            "intervalos": intervalos,
            "diasLivres": dias_livres
        }

def salvar_exemplo():
    exemplo_json = {
        "pessoa": {
            "nome": "Maria",
            "sobrenome": "Fernandes",
            "idade": 22,
            "periodo": "2022.2",
            "curso": "Engenharia de Software"
        },
        "materias": [
            {
                "nome": "Algoritmos e Programação",
                "creditos": 6,
                "dificuldade": 5,
                "professores": [
                    {"nome": "Prof. Carlos", "preferencia": 9},
                    {"nome": "Prof. Ana", "preferencia": 7}
                ],
                "horarios": [
                    {"inicio": "Segunda 08:00", "final": "Segunda 10:00", "preferencia": 8},
                    {"inicio": "Quarta 08:00", "final": "Quarta 10:00", "preferencia": 6}
                ]
            },
            {
                "nome": "Banco de Dados",
                "creditos": 4,
                "dificuldade": 6,
                "professores": [
                    {"nome": "Prof. João", "preferencia": 10}
                ],
                "horarios": [
                    {"inicio": "Terça 14:00", "final": "Terça 16:00", "preferencia": 9}
                ]
            }
        ],
        "preferenciasDeHorario": {
            "chegada_geral_mmi": {"maximo": "9:00", "minimo": "8:00", "ideal": "8:30"},
            "saida_geral_mmi": {"maximo": "19:00", "minimo": "18:00", "ideal": "18:30"},
            "chegada_especifica": [
                {"dia": 1, "mmi": {"maximo": "9:30", "minimo": "8:30", "ideal": "9:00"}}
            ],
            "saida_especifica": [
                {"dia": 3, "mmi": {"maximo": "18:30", "minimo": "17:30", "ideal": "18:00"}}
            ]
        },
        "cargaTotal": {
            "carga_total_geral_mmi": {"maximo": "8 horas", "minimo": "6 horas", "ideal": "7 horas"},
            "carga_especifica": [
                {"dia": 1, "mmi": {"maximo": "7 horas", "minimo": "5 horas", "ideal": "6 horas"}},
                {"dia": 3, "mmi": {"maximo": "9 horas", "minimo": "8 horas", "ideal": "8.5 horas"}}
            ]
        },
        "intervalos": {
            "intervalosEspecificos": [
                {"dias": [1, 2], "horario_inicio": "12:00", "horario_fim": "13:00", "prioridade": 5}
            ],
            "intervalosDistancia": [
                {"dias": [1, 2, 3], "distancia": 1, "repeticoes": 0, "prioridade": 10}
            ]
        },
        "creditos": {
            "creditos_mmi": {"maximo": 25, "minimo": 15, "ideal": 20}
        },
        "diasLivres": {
            "dias": [
                {"dia": 5, "prioridade": 10}  # Prioridade 10 significa que é essencial ter esse dia livre
            ]
        }
    }

    with open('configuracoes.json', 'w') as file:
        json.dump(exemplo_json, file)

# Executando Funções de Exemplo
if __name__ == '__main__':
    salvar_exemplo()
    config = carregar_configuracoes('configuracoes.json')
    
    pessoa = config["pessoa"]
    materias = config["materias"]
    preferencias_de_horario = config["preferenciasDeHorario"]
    carga_total = config["cargaTotal"]
    creditos = config["creditos"]
    intervalos = config["intervalos"]
    dias_livres = config["diasLivres"]

    # Imprimindo informações da pessoa
    print(f'Nome: {pessoa.nome} {pessoa.sobrenome}, Idade: {pessoa.idade}, Curso: {pessoa.curso}, Período: {pessoa.periodo}')
    
    # Imprimindo informações das matérias
    for materia in materias:
        print(f'Matéria: {materia.nome}, Créditos: {materia.creditos}, Dificuldade: {materia.dificuldade}')
        for professor in materia.possibilidades:
            for prof in professor.professores:
                print(f'  Professor: {prof.nome}, Preferência: {prof.preferencia}')
            for horario in professor.horarios:
                print(f'  Horário: {horario.inicio} - {horario.final}, Preferência: {horario.preferencia}')

    # Imprimindo preferências de horário
    print(f'Horário geral de chegada: {preferencias_de_horario.chegada_geral_mmi.minimo} - {preferencias_de_horario.chegada_geral_mmi.maximo}, Ideal: {preferencias_de_horario.chegada_geral_mmi.ideal}')
    print(f'Horário geral de saída: {preferencias_de_horario.saida_geral_mmi.minimo} - {preferencias_de_horario.saida_geral_mmi.maximo}, Ideal: {preferencias_de_horario.saida_geral_mmi.ideal}')
    
    for chegada in preferencias_de_horario.chegada_especifica:
        print(f'  Especificação de chegada para {chegada.dia}: {chegada.mmi.minimo} - {chegada.mmi.maximo}, Ideal: {chegada.mmi.ideal}')
    for saida in preferencias_de_horario.saida_especifica:
        print(f'  Especificação de saída para {saida.dia}: {saida.mmi.minimo} - {saida.mmi.maximo}, Ideal: {saida.mmi.ideal}')

    # Imprimindo informações de carga total
    print(f'Carga total geral: {carga_total.carga_total_geral_mmi.minimo} - {carga_total.carga_total_geral_mmi.maximo}, Ideal: {carga_total.carga_total_geral_mmi.ideal}')
    for carga in carga_total.carga_especifica:
        print(f'  Carga específica para {carga.dia}: {carga.mmi.minimo} - {carga.mmi.maximo}, Ideal: {carga.mmi.ideal}')

    # Imprimindo informações de créditos
    print(f'Créditos: Min: {creditos.creditos_mmi.minimo}, Max: {creditos.creditos_mmi.maximo}, Ideal: {creditos.creditos_mmi.ideal}')

    # Imprimindo intervalos específicos
    for intervalo in intervalos.intervalosEspecificos:
        print(f'Intervalo específico: {intervalo.dias} de {intervalo.horario_inicio} a {intervalo.horario_fim}, Prioridade: {intervalo.prioridade}')
    for distancia in intervalos.intervalosDistancia:
        print(f'Distância de intervalos para {distancia.dias}: Distância: {distancia.distancia}, Repetições: {distancia.repeticoes}, Prioridade: {distancia.prioridade}')

    # Imprimindo dias livres
    for dia in dias_livres.dias:
        print(f'Dia livre: {dia.dia}, Prioridade: {dia.prioridade}')

