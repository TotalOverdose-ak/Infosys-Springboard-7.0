package com.example.backend.services;

import com.example.backend.models.Subsidy;
import com.example.backend.repositories.SubsidyRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class SubsidyService {

    @Autowired
    private SubsidyRepository subsidyRepository;

    public List<Subsidy> getAllSubsidies() {
        return subsidyRepository.findAll();
    }

    public List<Subsidy> getSubsidies(String state, String category, String search, int limit) {
        return subsidyRepository.findByIsActiveTrue(state, category, search, limit);
    }

    public Subsidy getSubsidyById(String id) throws Exception {
        Optional<Subsidy> subsidy = subsidyRepository.findById(id);
        if (subsidy.isPresent()) {
            return subsidy.get();
        } else {
            throw new Exception("Subsidy not found with id: " + id);
        }
    }

    public Subsidy saveSubsidy(Subsidy subsidy) {
        return subsidyRepository.save(subsidy);
    }

    public Subsidy updateSubsidy(String id, Subsidy updatedSubsidy) {
        return subsidyRepository.findById(id).map(subsidy -> {
            subsidy.setTitle(updatedSubsidy.getTitle());
            subsidy.setDescription(updatedSubsidy.getDescription());
            subsidy.setAmount(updatedSubsidy.getAmount());
            subsidy.setEligibilityCriteria(updatedSubsidy.getEligibilityCriteria());
            subsidy.setApplicationDeadline(updatedSubsidy.getApplicationDeadline());
            subsidy.setState(updatedSubsidy.getState());
            subsidy.setCategory(updatedSubsidy.getCategory());
            subsidy.setActive(updatedSubsidy.isActive());
            subsidy.setDocumentsRequired(updatedSubsidy.getDocumentsRequired());
            try {
                return subsidyRepository.save(subsidy);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }).orElseThrow(() -> new RuntimeException("Subsidy not found with id " + id));
    }
}
