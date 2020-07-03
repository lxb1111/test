package com.baidu.main;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import java.io.Serializable;

public class SparkWriteParquet {
    public static class Person implements Serializable {

        private String name;
        private int age;
        private String city;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public int getAge() {
            return age;
        }

        public void setAge(int age) {
            this.age = age;
        }

        public String getCity() {
            return city;
        }

        public void setCity(String city) {
            this.city = city;
        }
    }

    public static void main(String[] args) {
        SparkSession spark = SparkSession.builder()
                .appName("SparkReadWriteParquet")
                .master("local")
                .getOrCreate();

        // Read test
        JavaRDD<Person> peopleRDD = spark.read()
                .textFile("test_parquet.csv")
                .javaRDD()
                .map((Function<String, Person>) line -> {
                    String[] parts = line.split(",");
                    Person person = new Person();
                    person.setName(parts[0]);
                    person.setAge(Integer.parseInt(parts[1].trim()));
                    person.setCity(parts[2].trim());
                    return person;
                });

        Dataset<Row> peopleDF = spark.createDataFrame(peopleRDD, Person.class);
        peopleDF.show();
        peopleDF.write().option("compression", "none")
                .mode("overwrite")
                .parquet("test_parquet");

        // Read Test
        Dataset<Row> test = spark.read().parquet("test_parquet");
        test.schema();
        test.show();
    }



}
