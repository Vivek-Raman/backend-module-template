import argparse
import os
import re

target_version = '1.0-rc1'
spring_boot_version = '3.1.4'

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
      print(f'{"[DRY RUN] Replaces" if args.dry_run else "[*] Replaced"} "{match.group(0)}" with "{replace_text}" at {filepath}')
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
  dir_path = os.path.dirname(orig_path)
  new_path = os.path.join(dir_path, new_name)

  if os.path.exists(new_path):
    os.removedirs(new_path)

  if not args.dry_run:
    os.renames(orig_path, new_path)
  print(f"{'[DRY RUN] Renames' if args.dry_run else '[*] Renamed'} {orig_path} to {new_path}")


def main():
  args = parse_arguments()
  if not args.dry_run:
    print('WARNING: --dry-run is not set. Files will be updated. Are you sure you want to continue?')
    print(f'Module name: {args.name}')
    print(f'Module name (lowerCamelCase): {get_lower_camel_case(args.name)}')
    print(f'Module name (UpperCamelCase): {get_upper_camel_case(args.name)}')
    print(f'Module name (directory/name): {get_directory_name(args.name)}')
    print(f'Module name (package.name): {get_package_name(args.name)}')
    print('')
    go_ahead = input(f'Continue? (y/N) ')
    if not go_ahead or go_ahead.lower() != 'y':
      print('Aborting.')
      return

  print(f'Updating version numbers...')
  find_and_replace(args, './module-app/pom.xml', '<version>[rc\\d\\-\\.]+</version>', f'<version>{target_version}</version>')
  find_and_replace(args, './template/pom.xml', '<version>[rc\\d\\-\\.]+</version>', f'<version>{target_version}</version>')
  find_and_replace(args, './pom.xml', '<version>[rc\\d\\-\\.]+</version>', f'<version>{target_version}</version>')
  find_and_replace(args, './pom.xml', '<artifactId>spring-boot-starter-parent</artifactId>\\n\\t\\t<version>[rc\\d\\-\\.]+</version>', f'<artifactId>spring-boot-starter-parent</artifactId>\\n\\t\\t<version>{spring_boot_version}</version>')

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
  find_and_replace(args, './module-app/src/', 'spring.profiles.include=module', f'spring.profiles.include={args.name}')

  print(f'Renaming classes...')
  rename(args, './template/src/main/java/dev/vivekraman/module/config/ModuleConfig.java', f'{get_upper_camel_case(args.name)}Config.java')
  rename(args, './module-app/src/main/java/dev/vivekraman/module/app/BackendModuleTemplateApplication.java', f'BackendModule{get_upper_camel_case(args.name)}Application.java')

  print(f'Renaming class directories...')
  rename(args, './module-app/src/main/java/dev/vivekraman/module', get_directory_name(args.name))
  rename(args, './module-app/src/test/java/dev/vivekraman/module', get_directory_name(args.name))
  rename(args, './template/src/main/java/dev/vivekraman/module', get_directory_name(args.name))

  print(f'Renaming resources...')
  rename(args, './module-app/src/main/resources/application-module.properties', f'application-{args.name}.properties')

  print(f'Renaming modules...')
  rename(args, './template', f'{args.name}')
  rename(args, './module-app', f'{args.name}-app')

  if args.dry_run:
    print('Completed dry run. Remove --dry-run from the arguments to apply these changes.')
  else:
    print(f'Completed! You can now delete this script. Happy hacking!')


if __name__ == '__main__':
  main()
