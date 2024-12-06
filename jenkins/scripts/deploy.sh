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


## Database Part
mysqldump -h localhost -u root -p'redhat' --routines employee_management_db > /home/employeemanagement/DEPLOYMENT-BACKUPS/$(date +%F)/employee_management_db-${deploy_bkup_date}.sql
if [[ "$?" -eq "0" ]];
then
        mysql -h localhost -u root -p'redhat' -e "DROP DATABASE employee_management_db;"
        mysql -h localhost -u root -p'redhat' -e "CREATE DATABASE employee_management_db;"
        mysql -h localhost -u root -p'redhat' employee_management_db < /home/employeemanagement/employee_management/data.sql
fi
touch /home/employeemanagement/employee_management/employee_management/wsgi.py

set +x
