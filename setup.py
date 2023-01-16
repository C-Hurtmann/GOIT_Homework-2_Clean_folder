from setuptools import setup, find_namespace_packages


setup(name='GOIT_homework_2_clean-folder_ZCO',
      version='0.3.2',
      description='Sort specified folder to subfolders by their suffix (other subfolders will be disposed). Rename files to ASCII format. Unpack the archives',
      url='https://github.com/C-Hurtmann/GOIT_Homework-2_Clean_folder',
      license='MIT',
      classifiers=['Programming Language :: Python :: 3', 
                  'License :: OSI Approved :: MIT License', 
                  'Operating System :: OS Independent'],
      author='Constantine Zagorodnyi',
      author_email='Constantine2903@gmail.com',
      packages=find_namespace_packages(), 
      entry_points={'console_scripts':['clean-folder=clean_folder.clean:main']}
)
