package com.example.backend.seeders;

import com.example.backend.models.Subsidy;
import com.example.backend.repositories.SubsidyRepository;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.io.InputStream;
import java.util.List;

@Component
public class DataSeeder implements CommandLineRunner {

    @Autowired
    private SubsidyRepository subsidyRepository;

    @Override
    public void run(String... args) throws Exception {
        // Only seed if database is completely empty (first run)
        // Do NOT deleteAll - we have dynamic data from the pipeline!
        try {
            long count = subsidyRepository.count();
            if (count > 0) {
                System.out.println("==========================================================");
                System.out.println("DB already has " + count + " schemes. Skipping seed.");
                System.out.println("==========================================================");
                return;
            }

            ObjectMapper mapper = new ObjectMapper();
            mapper.registerModule(new JavaTimeModule());
            InputStream inputStream = TypeReference.class.getResourceAsStream("/schemes.json");

            List<Subsidy> schemes = mapper.readValue(inputStream, new TypeReference<List<Subsidy>>() {});
            subsidyRepository.saveAll(schemes);

            System.out.println("==========================================================");
            System.out.println("Loaded " + schemes.size() + " schemes from JSON (first run).");
            System.out.println("==========================================================");
        } catch (Exception e) {
            System.err.println("Seed skipped (DB connection issue): " + e.getMessage());
        }
    }
}
