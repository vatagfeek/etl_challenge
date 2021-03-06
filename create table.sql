DROP TABLE employee, department, updated_salaries;

CREATE TABLE department (
   "id" UUID DEFAULT uuid_generate_v1() NOT NULL,
   name TEXT,
   salary_increment TEXT,
   PRIMARY KEY (id)
);


CREATE TABLE employee (
   "id" UUID DEFAULT uuid_generate_v1() NOT NULL,
   first_name TEXT,
   last_name TEXT,
   salary NUMERIC,
   department_id UUID,
   PRIMARY KEY (id),
   FOREIGN KEY (department_id)
      REFERENCES department (id)
);


CREATE TABLE updated_salaries (
   employee_id UUID,
   updated_salary NUMERIC
);
