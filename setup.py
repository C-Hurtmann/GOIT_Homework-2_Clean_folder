from setuptools import setup


setup(name='clean folder',
      version='1.1',
      description='Sort specified folder to subfolders by their suffix (other subfolders will be disposed). Rename files to ASCII format. Unpack the archives',
      url='https://github.com/C-Hurtmann/Clean_folder',
      author='Constantine Zagorodnyi',
      author_email='Constantine2903@gmail.com',
      packages='clean_folder', 
      entry_points={'console_scripts':'clean-folder=clean_folder.clean:main'}
)
