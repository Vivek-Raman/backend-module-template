import argparse
import os
import re
import subprocess

target_version = '1.0-rc1'

def parse_arguments():
  parser = argparse.ArgumentParser(description='Backend module setup template')
  parser.add_argument('--name', required=True, type=str, help='Name of the module')
  parser.add_argument('--dry-run', action='store_true', help='Logs changes instead of applying them')
  args = parser.parse_args()
  return args


def get_lower_camel_case(text):
  # Split by hyphens or spaces
  words = re.split('-', text)
  # First word in lowercase, rest capitalized
  return words[0].lower() + ''.join(word.title() for word in words[1:])


def get_upper_camel_case(text):
  camel = get_lower_camel_case(text)
  return camel[0].upper() + camel[1:]


def get_package_name(name):
  return str(name).replace('-', '.')


def get_directory_name(name):
  return str(name).replace('-', '/')


def do_fnr(args, filepath, find_text, replace_text):
  try:
    # Read the content
    with open(filepath, 'r', encoding='utf-8') as f:
      content = f.read()

    match = re.search(find_text, content)
    if not match:
      return

    modified_content = re.sub(find_text, replace_text, content)

    # Only write if there are actual changes and content isn't empty
    if modified_content and modified_content != content:
      if not args.dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
          f.write(modified_content)
      print(f'{"[DRY RUN] Replaces" if args.dry_run else "Replaced"} "{match.group(0)}" with "{replace_text}" at {filepath}')
    else:
      print(f'No changes needed in {filepath}')
  except Exception as e:
    print(f'Error processing {filepath}: {str(e)}')


def find_and_replace(args, path, find_text, replace_text):
  if os.path.isfile(path):
    do_fnr(args, path, find_text, replace_text)
    return

  for root, dirs, files in os.walk(path):
    for file in files:
      filepath = os.path.join(root, file)
      do_fnr(args, filepath, find_text, replace_text)


def rename(args, orig_path, new_name):
  if not os.path.exists(orig_path):
    print(f"Path does not exist: {orig_path}")
    return False

  dir_path = os.path.dirname(orig_path)
  new_path = os.path.join(dir_path, new_name)

  if os.path.exists(new_path):
    print(f"Cannot rename: target already exists: {new_path}")
    return False

  if not args.dry_run:
    os.rename(orig_path, new_path)
  print(f"{'[DRY RUN] Renames' if args.dry_run else 'Renamed'} {orig_path} to {new_path}")
  return True


def main():
  args = parse_arguments()

  print(f'Updating version numbers...')
  find_and_replace(args, './module-app/pom.xml', '<version>.+</version>', f'<version>{target_version}</version>')
  find_and_replace(args, './template/pom.xml', '<version>.+</version>', f'<version>{target_version}</version>')
  find_and_replace(args, './pom.xml', '<version>.+</version>', f'<version>{target_version}</version>')

  print(f'Updating parent artifact IDs...')
  find_and_replace(args, './module-app/pom.xml', '<artifactId>backend-module-template</artifactId>', f'<artifactId>backend-module-{args.name}</artifactId>')
  find_and_replace(args, './template/pom.xml', '<artifactId>backend-module-template</artifactId>', f'<artifactId>backend-module-{args.name}</artifactId>')
  find_and_replace(args, './pom.xml', '<artifactId>backend-module-template</artifactId>', f'<artifactId>backend-module-{args.name}</artifactId>')

  print(f'Updating module artifact IDs...')
  find_and_replace(args, './module-app/pom.xml', '<artifactId>module-app</artifactId>', f'<artifactId>{args.name}-app</artifactId>')
  find_and_replace(args, './template/pom.xml', '<artifactId>template</artifactId>', f'<artifactId>{args.name}</artifactId>')

  print(f'Updating modules and dependencies...')
  find_and_replace(args, './module-app/pom.xml', '<artifactId>template</artifactId>', f'<artifactId>{args.name}</artifactId>')
  find_and_replace(args, './pom.xml', '<module>template</module>', f'<module>{args.name}</module>')
  find_and_replace(args, './pom.xml', '<module>module-app</module>', f'<module>{args.name}-app</module>')
  find_and_replace(args, './pom.xml', '<artifactId>template</artifactId>', f'<artifactId>{args.name}</artifactId>')

  print(f'Updating artifact properties...')
  find_and_replace(args, './pom.xml', '<name>backend-module-template</name>', f'<name>backend-module-{args.name}</name>')

  print(f'Updating package declarations...')
  find_and_replace(args, './module-app/src/', 'package dev.vivekraman.module', f'package dev.vivekraman.{get_package_name(args.name)}')
  find_and_replace(args, './template/src/', 'package dev.vivekraman.module', f'package dev.vivekraman.{get_package_name(args.name)}')

  print(f'Updating package imports...')
  find_and_replace(args, './module-app/src/', 'import dev.vivekraman.module', f'import dev.vivekraman.{get_package_name(args.name)}')
  find_and_replace(args, './template/src/', 'import dev.vivekraman.module', f'import dev.vivekraman.{get_package_name(args.name)}')

  print(f'Updating classes...')
  find_and_replace(args, './template/src/', 'public GroupedOpenApi moduleApiGroup()', f'public GroupedOpenApi {get_lower_camel_case(args.name)}ApiGroup()')
  find_and_replace(args, './template/src/', '.packagesToScan("dev.vivekraman.module.controller")', f'.packagesToScan("dev.vivekraman.{get_package_name(args.name)}.controller")')
  find_and_replace(args, './template/src/', 'public class ModuleConfig', f'public class {get_upper_camel_case(args.name)}Config')
  find_and_replace(args, './template/src/', 'String MODULE_NAME = "module";', f'String MODULE_NAME = "{args.name}";')
  find_and_replace(args, './module-app/src/', 'public class BackendModuleTemplateApplication', f'public class BackendModule{get_upper_camel_case(args.name)}Application')
  find_and_replace(args, './module-app/src/', 'SpringApplication.run(BackendModuleTemplateApplication.class, args)', f'SpringApplication.run(BackendModule{get_upper_camel_case(args.name)}Application.class, args);')

  print(f'Updating properties...')
  find_and_replace(args, './module-app/src/', 'spring.profiles.include=module', f'spring.profiles.include=module{args.name}')

  print(f'Renaming class directories...')
  rename(args, './module-app/src/main/java/dev/vivekraman/module', get_directory_name(args.name))

  print(f'Installing...')
  if not args.dry_run:
    print('Running mvn clean install -U...')
    subprocess.run(['mvn', 'clean', 'install', '-U'], check=True)
  else:
    print('[DRY RUN] Would run: mvn clean install -U')

  if args.dry_run:
    print('Completed dry run. Remove --dry-run from the arguments to apply these changes.')
  else:
    print(f'Completed! You can now delete this script. Happy hacking!')


if __name__ == '__main__':
  main()
