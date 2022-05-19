#!/usr/bin/env python3

import glob
import pprint
from pathlib import Path


class MarkdownPageBuilder:
    def __init__(self):
        self.index_markdown_file_path = 'index.md'
        self.structure = dict()

    def add_header(self, file_path, group_name, service_name, header):
        group_name = group_name.replace('-', ' ').title().strip()
        if group_name not in self.structure.keys():
            self.structure[group_name] = dict()

        services = self.structure[group_name]
        if service_name not in services.keys():
            services[service_name] = dict()

        service = services[service_name]
        if 'file' not in service or 'headers' not in service:
            service['file'] = file_path  # will be used to create the link to the anchor on the specific page
            service['headers'] = list()
        else:
            service['headers'].append(header.strip())

    def print_structure(self):
        pprint.pprint(self.structure)  # used for debugging purpose

    def write(self):
        with open(self.index_markdown_file_path, 'w') as file:
            file.write("# AWS notes  \n")

            for group_key, group_value in self.structure.items():
                file.write(f'## {group_key}  \n')

                for services_key, services_value in group_value.items():
                    file_path = services_value['file']

                    # manually create a hierarchy using 4 spaces for the services
                    file.write(f'### {services_key}  \n')

                    for header in services_value['headers']:
                        hashtag_count = header.count('#')
                        header = header.replace('#', '').strip()

                        # 4 spaces per hashtag found in the header
                        file.write((4 * hashtag_count) * '&nbsp;' +
                                   f'[{header}]({file_path}#{header.replace(" ", "-").replace("(", "").replace(")", "").lower()})  \n')
                file.write(f'\n___\n')


def specific_concept(readme_file_path, content_keywords):
    for keyword in content_keywords:
        if keyword in readme_file_path:
            return True
    return False


def main():
    build_dir = Path("./build")
    build_dir.mkdir(exist_ok=True)
    page_builder = MarkdownPageBuilder()

    complete_notes_path = build_dir/'complete.md'
    if complete_notes_path.is_file():
        complete_notes_path.unlink()

    archi_notes_path = build_dir/'archi.md'
    if archi_notes_path.is_file():
        archi_notes_path.unlink()
    archi_content_keywords = [
        "analytics",
        "application-integration",
        "cli-sdk",
        "compute",
        "containers",
        "cost-management",
        "database",
        "developer-tools",
        "end-user-computing"
        "frontend-mobile",
        "general-info",
        "management-governance",
        "migration-transfer",
        "network-content-delivery",
        "security-identity-compliance",
        "storage"
    ]

    devops_notes_path = build_dir/'devops.md'
    if devops_notes_path.is_file():
        devops_notes_path.unlink()
    devops_content_keywords = [
        "compute",
        "cli-sdk",
        "developer-tools",
        "route53",
        "vpc",
        "transit-gateway",
        "s3",
        "general-info",
        "containers",
        "compute",
        "cloudformation",
        "cloudtrail",
        "cloudwatch",
        "opsworks"
    ]

    ml_notes_path = build_dir/'ML.md'
    if ml_notes_path.is_file():
        ml_notes_path.unlink()
    ml_content_keywords = [
        "machine-learning",
        "analytics",
        "batch"
    ]

    big_data_notes_path = build_dir/'big_data.md'
    if big_data_notes_path.is_file():
        big_data_notes_path.unlink()
    big_data_content_keywords = [
        "internet-of-things",
        "analytics",
        "big-data",
        "migration-transfer",
        "database",
        "greengrass",
        "kinesis",
        "direct-connect",
        "s3",
        "lambda",
        "iam",
        "cloudtrail",
        "aml"
    ]

    readme_count = 0

    # find all README.md files recursively
    for readme_file_path in glob.iglob('./services/**/*.md', recursive=True):
        readme_count += 1

        # first add the full content of the file in the merged README.md
        with open(readme_file_path, 'r') as service_file, \
                open(complete_notes_path, 'a') as complete_notes_file, \
                open(ml_notes_path, 'a') as ml_notes_file, \
                open(devops_notes_path, 'a') as devops_notes_file, \
                open(archi_notes_path, 'a') as archi_notes_file, \
                open(big_data_notes_path, 'a') as big_data_file:
            service_content = service_file.read()

            # write content to complete notes
            complete_notes_file.write(service_content)
            complete_notes_file.write('\n\n')

            # check if it is an archi certification concept and add it
            if specific_concept(readme_file_path, archi_content_keywords):
                archi_notes_file.write(service_content)
                archi_notes_file.write('\n\n')

            # check if it is a devops certification concept and add it
            if specific_concept(readme_file_path, devops_content_keywords):
                devops_notes_file.write(service_content)
                devops_notes_file.write('\n\n')

            # check if it is an ML certification concept and add it
            if specific_concept(readme_file_path, ml_content_keywords):
                ml_notes_file.write(service_content)
                ml_notes_file.write('\n\n')

            # check if it is a big data certification concept and add it
            if specific_concept(readme_file_path, big_data_content_keywords):
                big_data_file.write(service_content)
                big_data_file.write('\n\n')

        # figure out the hierarchy, service are in groups (compute, storage, ...) while other generic info are not
        folders_count = readme_file_path.count('/')
        if folders_count == 3:
            # found general info folder
            previous_path, services, service_name, file = readme_file_path.split('/')
            service_group = 'general'
        elif folders_count == 4:
            # found a service
            previous_path, services, service_group, service_name, file = readme_file_path.split('/')
        else:
            raise Exception('Unexpected folder hierarchy')

        # open found README.md and extract the headers
        with open(readme_file_path, 'r') as readme_file:
            for line in readme_file:
                if line and line.strip().startswith("#"):
                    # found a header
                    if line.count('#') == 1:
                        # if we encountered the first header, do not count it as a header and use it as the service name
                        # Will be used as the separator between all services
                        service_name = line.replace('#', '').strip()
                    page_builder.add_header(readme_file_path, service_group, service_name, line)

    print(f'\nNumber of README.md files processed : {readme_count}\n')
    print("\nStructure found in the directories.")
    page_builder.print_structure()

    print(f'\nWriting the created index into README.md...')
    page_builder.write()
    print("Done. Exiting.")


if __name__ == '__main__':
    main()

