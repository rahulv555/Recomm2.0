package com.recomm.recommservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.kafka.annotation.EnableKafka;

@SpringBootApplication
@EnableKafka
public class RecommserviceApplication {

	public static void main(String[] args) {
		SpringApplication.run(RecommserviceApplication.class, args);
	}

}
