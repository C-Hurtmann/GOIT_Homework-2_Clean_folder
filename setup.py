from setuptools import setup, find_namespace_packages


setup(name='clean-folder_from_ZCO',
      version='0.1.2',
      description='Sort specified folder to subfolders by their suffix (other subfolders will be disposed). Rename files to ASCII format. Unpack the archives',
      url='https://github.com/C-Hurtmann/Clean_folder',
      license='MIT',
      classifiers=['Programming Language :: Python :: 3', 
                  'License :: OSI Approved :: MIT License', 
                  'Operating System :: OS Independent']
      author='Constantine Zagorodnyi',
      author_email='Constantine2903@gmail.com',
      packages=find_namespace_packages(), 
      entry_points={'console_scripts':'clean-folder=clean_folder.clean:main'}
)
