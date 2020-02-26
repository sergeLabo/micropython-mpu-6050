#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#######################################################################
# Copyright (C) La Labomedia August 2018
#
# This file is part of pymultilame.

# pymultilame is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pymultilame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pymultilame.  If not, see <https://www.gnu.org/licenses/>.
#######################################################################


"""
Des outils pratiques fait avec le package pathlib
    https://docs.python.org/3/library/pathlib.html

The pathlib module describes itself as a way to:
    Parse, build, test, and otherwise work on filenames and paths
    using an object-oriented API instead of low-level string operations.

"""


import os
from pathlib import Path, PosixPath
import shutil


class PathTools:

    def create_directory(self, directory):
        """
        Crée le répertoire avec le chemin absolu.
        ex: /media/data/3D/projets/meteo/meteo_forecast/2017_06
        """

        try:
            pathlib.Path(directory).mkdir(mode=0o777, parents=False)
            print("Création du répertoire: {}".format(directory))
        except FileExistsError as e:
            print("Ce répertoire existe: {}".format(directory))
        except PermissionError as e:
            print("Problème de droits avec le répertoire: {}".format(directory))
        except:
            print("Erreur avec le répertoire: {}".format(directory))

    def get_current_directory(self):
        """
        Retourne le string du chemin absolu du dossier du script.
        Ne marche pas dans Blender:
            - retourne le dossier du blend avec le Standalone Player
            - retourne le home dans le Embedded Player
        """

        root =  str(Path.cwd().resolve())
        print("Chemin du dossier courant de ce script:", root)

        return root

    def get_file_list(self, directory, extentions):
        """Retourne la liste de tous les fichiers avec les extentions de
        la liste extentions
        extentions = liste = ["mid", "midi"]]

        Si directory est défini avec chemin relatif (idem avec absolu),
            les fichiers sont avec chemin relatif (idem avec absolu).

        Attention: subdirs comprend le dossier racine !
        """

        file_list = []
        for path, subdirs, files in os.walk(directory):
            for name in files:
                for extention in extentions:
                    if name.endswith(extention):
                        file_list.append(str(Path(path, name)))

        return file_list

    def get_project_sub_directory(self, mon_projet):
        """Le dossier projet est "toto", avec seulement License, lanceur, ...
        Tout le projet lui-même est dans un sous-dossier appelé ici
            "mon_projet"
        Il est possible de renommer le dossier du projet, exemple toto-master.
        Mais les autres dossiers et fichiers de ce dossier ne doivent pas être
        modifié.
        Le sous-dossier peut s'appeler "toto".

        Dans pymultilame, le sous-dossier est pymultilame
        Retourne le chemin absolu de mon_projet.
        """

        p = Path(mon_projet)

        return p

    def create_path(self):
        """
        os.path.join(path, *paths)
        """
        pass

    def get_current_directory_contents(self):
        """
        The dot (".") defines the current directory.
        The iterdir() method returns an iterator that yields the names
        of all the files.
        for d in currentDirectory.iterdir():
            print(d)
        """
        # TODO finir
        return Path('.')

    def construct_path(self):
        """
        https://docs.python.org/3/library/pathlib.html#basic-use
        """

        return Path.home() / 'python' / 'scripts' / 'test.py'

    def opening_file(self, fichier):
        p = Path('./')
        q = p / fichier
        with q.open() as f:
            lines = f.readlines()
        return lines

    def set_extension(self, fichier, extension):
        """Ajoute une extention:
        fichier est Path ou pas
        extension = ".toto"
        Retourne toujours un path
        """

        if not isinstance(fichier, PosixPath):
            fichier = Path(fichier)

        return fichier.with_suffix(extension)

    def path_to_str(self, fichier):
        """Convertit un objet Path en string.
        Cette fonction sert juste à retrouver la syntaxe.
        """

        return str(fichier)

    def change_directory(self, fichier):
        """fichier est Path ou pas
        """

        if not isinstance(fichier, PosixPath):
            fichier = Path(fichier)
        f = fichier.absolute()
        print(f.resolve())


class ShUtil:

    def copy_file(self, src, dst):
        """Copie le fichier src à dst
        src, dst sont les noms avec le chemin des fichiers.
        Marche avec src, dst en Path ou pas
        """

        shutil.copyfile(src, dst)


class Developper:

    def get_list_method_in_class(self, Foo):
        """
        Voir ?
        from optparse import OptionParser
        import inspect
        inspect.getmembers(OptionParser, predicate=inspect.ismethod)
        ou
        for att in dir(your_object):
            print (att, getattr(your_object,att))
        """

        method_list = [func for func in dir(Foo) \
                       if callable(getattr(Foo, func)) \
                       and not func.startswith("__")]
        return method_list


if __name__ == "__main__":

    pt = PathTools()
    su = ShUtil()
    dev = Developper()

    pt.get_current_directory()

    print(pt.get_file_list("./", ".py"))

    d = "/media/data/3D/projets/pymultilame/pymultilame"
    print(pt.get_file_list(d, ".py"))

    for d in Path('.').iterdir():
        print(d)

    m = dev.get_list_method_in_class(PathTools)
    print(m)

    a = pt.get_project_sub_directory("pymultilame")
    print("sub_directory", a)

    e = Path('/media')
    f = e / 'data' / '3D' / 'projets' / 'darknet-letters'
    print("file_list =", pt.get_file_list(f, [".py"]))

    print("Chemin du home", Path.home())

    c = pt.construct_path()
    print("Exemple de construction d'un chemin", c)

    lines = pt.opening_file('mytools.py')
    print(lines[0])

    # Changement d'extension
    f = pt.set_extension('mytools.py', '.toto')
    print('mytools.py de type', type('mytools.py'), 'devient',
            f, "de type", type(f))

    # Conversion Path to str
    print(pt.path_to_str(f), type(pt.path_to_str(f)))

    # Copie avec fichier en Path
    print("Copie de", type('mytools.py'), "vers", type(f))
    copyfile('mytools.py', f)

    copyfile(Path('mytools.py'), str(pt.set_extension('mytools.py', '.moi')))

    pt.change_directory('mytools.py')
