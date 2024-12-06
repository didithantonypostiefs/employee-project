#!/usr/bin/env sh

echo 'Deploying employee-project'
set -x
## Deploy Code from GITHUB
cd /home/employeemanagement
deploy_bkup_date=$(date +%F-%T)
mkdir -pv /home/employeemanagement/DEPLOYMENT-BACKUPS/$(date +%F)
git clone https://github.com/didithantonypostiefs/employee-project.git
mv -v /home/employeemanagement/employee_management /home/employeemanagement/DEPLOYMENT-BACKUPS/$(date +%F)/employee_management-${deploy_bkup_date}
mv -v /home/employeemanagement/employee-project/employee_management /home/employeemanagement/
rm -rvf /home/employeemanagement/employee-project
cp -av /home/employeemanagement/DEPLOYMENT-BACKUPS/$(date +%F)/employee_management-${deploy_bkup_date}/employee_management/settings.py /home/employeemanagement/employee_management/employee_management/settings.py

/home/employeemanagement/employee_managementenv/bin/python /home/employeemanagement/employee_management/manage.py collectstatic
rsync -av /home/employeemanagement/employee_management/assets/admin /home/employeemanagement/employee_management/static/
set +x
