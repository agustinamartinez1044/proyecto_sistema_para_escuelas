#Sistema para escuelas por Agustina Martinez

# -*- coding: utf-8 -*-
import csv
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

#Se crea el motor y la base declarativa
engine=create_engine('sqlite:///:memory:')
Base=declarative_base(engine)

#Se crea la clase Estudiante con sus respectivas relaciones
class Estudiante(Base):
    __tablename__="alumno"   

    id=Column(Integer,Sequence('alumno_seq_id'),primary_key=True)
    nombrea=Column(String)
    apellidoa=Column(String)
    curso_ida=Column(Integer,ForeignKey('curso.id'))
    
    #Se relaciona a los cursos
    cursos=relationship("Course",back_populates='estudiantes') 
    def __repr__(self):
        return'{}{}'.format(self.nombrea, self.apellidoa)

#Se crea la clase Course con sus respectivas relaciones 
class Course(Base):
    __tablename__='curso'

    id=Column(Integer, Sequence('curso_seq_id'),primary_key=True)
    nombrec=Column(String)

    #Se relaciona con los alumnos 
    estudiantes=relationship("Estudiante",back_populates='cursos') 
    #Se relaciona con los horarios
    hora_curso=relationship("Horario",back_populates='curso_hora') 
    def __repr__(self):
        return'{}'.format(self.nombrec)

#Se crea la clase Horario con sus respectivas relaciones
class Horario(Base):
    __tablename__='horario'

    id=Column(Integer, Sequence('horario_seq_id'),primary_key=True)
    dia=Column(String)
    hora_inicio=Column(String)
    hora_fin=Column(String)
    profesor_id=Column(Integer,ForeignKey('profesor.id'))
    curso_id=Column(Integer,ForeignKey('curso.id'))
    
    #Se relaciona con los cursos
    curso_hora=relationship("Course",back_populates='hora_curso') 
    #Se relaciona con los docentes
    curso_profe=relationship("Docente",back_populates='profe_curso') 
    def __repr__(self):
        return'{}{}{}'.format(self.dia,self.hora_inicio, self.hora_fin)

#Se crea la clase Docente con sus respectivas relaciones
class Docente(Base):
    __tablename__='profesor'

    id=Column(Integer, Sequence('profesor_seq_id'),primary_key=True)
    nombrep=Column(String)
    apellidop=Column(String)
    
    #Se relaciona con los horarios
    profe_curso=relationship("Horario",back_populates='curso_profe') 
    def __repr__(self):
        return'{}{}'.format(self.nombrep, self.apellidop)

#Se crea todas las tablas con el motor
Base.metadata.create_all(engine)

#Se crea la sesion
Session=sessionmaker(bind=engine)
session=Session()

#Se crean los estudiantes
alumno1=Estudiante(nombrea='Manuel ', apellidoa='Santos')
alumno2=Estudiante(nombrea='Roberto ', apellidoa= 'Muñoz')
alumno3=Estudiante(nombrea='Maria ', apellidoa= 'Garcia')
alumno4=Estudiante(nombrea='Eva ', apellidoa= 'Rodriguez')
alumno5=Estudiante(nombrea='Marcos ', apellidoa='Borjas')

#Se agregan los estudiantes a la base de datos
session.add_all([alumno1, alumno2, alumno3, alumno4, alumno5])

#Se asignan los estudiantes a los cursos
alumno1.cursos=Course(nombrec='Fisica')
alumno2.cursos=Course(nombrec='Id. Español')
alumno3.cursos=Course(nombrec='Matematica')
alumno4.cursos=Course(nombrec='Fisica')
alumno5.cursos=Course(nombrec='Quimica')


#Se crean los horarios
horario1=Horario(dia='Lunes: ',hora_inicio='08:00 am a ', hora_fin='09:30 am')
horario2=Horario(dia='Lunes: ', hora_inicio='09:40 am a ', hora_fin='10:45 pm')
horario3=Horario(dia='Lunes: ', hora_inicio='10:55 am a ', hora_fin='12:00 pm')
horario4=Horario(dia='Martes: ', hora_inicio='08:30 am a ', hora_fin='10:00 am')
horario5=Horario(dia='Martes: ', hora_inicio='10:10 am a ', hora_fin='12:00 am')


#Se agregan los horarios a la base de datos
session.add_all([horario1, horario2, horario3, horario4])

#Se asignan los horarios a los cursos y docentes
horario1.curso_hora=Course(nombrec='Ingles')
horario1.curso_profe=Docente(nombrep='Ana ',apellidop='Marcial')

horario2.curso_hora=Course(nombrec='Quimica')
horario2.curso_profe=Docente(nombrep='Paola ', apellidop='Cruz')

horario3.curso_hora=Course(nombrec='Matematica')
horario3.curso_profe=Docente(nombrep='Alejandro ', apellidop='Beltran')

horario4.curso_hora=Course(nombrec='Historia')
horario4.curso_profe=Docente(nombrep='Nelson ', apellidop='Contreras')

horario5.curso_hora=Course(nombrec='Historia')
horario5.curso_profe=Docente(nombrep='Nelson ', apellidop='Contreras')

#Se imprime el docente del horario 1
print(horario1.curso_profe)

#Se imprime el curso del horario 2
print(horario2.curso_hora)
#Se imprime el curso del horario 3
print(horario3.curso_hora)

#Se imprime nombre y apellido de todos los estudiantes
print(session.query(Estudiante).filter(Course.estudiantes.any()).all())

#Se imprime todos los horarios
print(session.query(Horario).filter(Docente.profe_curso.any()).all())

session.commit()