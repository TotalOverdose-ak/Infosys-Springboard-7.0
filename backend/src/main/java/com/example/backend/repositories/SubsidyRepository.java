package com.example.backend.repositories;

import com.example.backend.models.Subsidy;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class SubsidyRepository {

    private List<Subsidy> subsidies = new ArrayList<>();

    @PostConstruct
    public void init() {
        try {
            ObjectMapper mapper = new ObjectMapper();
            InputStream is = new ClassPathResource("data/schemes.json").getInputStream();
            subsidies = mapper.readValue(is, new TypeReference<List<Subsidy>>() {});
            System.out.println("Loaded " + subsidies.size() + " schemes from JSON successfully!");
        } catch (Exception e) {
            System.err.println("Error loading schemes JSON: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public long count() {
        return subsidies.size();
    }

    public Subsidy save(Subsidy subsidy) {
        if (subsidy.getId() == null) {
            subsidy.setId(UUID.randomUUID().toString());
        }
        subsidies.add(subsidy);
        return subsidy;
    }

    public Optional<Subsidy> findById(String id) {
        return subsidies.stream().filter(s -> id.equals(s.getId())).findFirst();
    }

    public void saveAll(List<Subsidy> newSubsidies) {
        for (Subsidy s : newSubsidies) {
            save(s);
        }
    }

    public List<Subsidy> findAll() {
        return new ArrayList<>(subsidies);
    }

    public List<Subsidy> findAll(int limit) {
        return subsidies.stream().limit(limit).collect(Collectors.toList());
    }

    public List<Subsidy> findByIsActiveTrue(String state, String category, String search, int limit) {
        return subsidies.stream()
            .filter(s -> {
                boolean match = s.isActive();
                if (state != null && !state.isEmpty() && !state.equalsIgnoreCase("All States")) {
                    match = match && state.equalsIgnoreCase(s.getState());
                }
                if (category != null && !category.isEmpty() && !category.equalsIgnoreCase("All Categories")) {
                    match = match && category.equalsIgnoreCase(s.getCategory());
                }
                if (search != null && !search.isEmpty()) {
                    String searchLower = search.toLowerCase();
                    boolean titleMatch = s.getTitle() != null && s.getTitle().toLowerCase().contains(searchLower);
                    boolean descMatch = s.getDescription() != null && s.getDescription().toLowerCase().contains(searchLower);
                    match = match && (titleMatch || descMatch);
                }
                return match;
            })
            .limit(limit)
            .collect(Collectors.toList());
    }

    public List<Subsidy> findByStateAndIsActiveTrue(String state) {
        return findByIsActiveTrue(state, null, null, 100);
    }

    public List<Subsidy> findByCategoryAndIsActiveTrue(String category) {
        return findByIsActiveTrue(null, category, null, 100);
    }

    public List<Subsidy> findByStateAndCategoryAndIsActiveTrue(String state, String category) {
        return findByIsActiveTrue(state, category, null, 100);
    }
}
