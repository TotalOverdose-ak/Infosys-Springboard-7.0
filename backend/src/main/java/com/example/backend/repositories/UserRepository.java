package com.example.backend.repositories;

import com.example.backend.models.User;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class UserRepository {

    private final List<User> users = new ArrayList<>();

    public void save(User user) {
        if (user.getId() == null) {
            user.setId(UUID.randomUUID().toString());
        }
        users.add(user);
    }

    public Optional<User> findByEmail(String email) {
        return users.stream().filter(u -> email.equals(u.getEmail())).findFirst();
    }

    public boolean existsByEmail(String email) {
        return users.stream().anyMatch(u -> email.equals(u.getEmail()));
    }

    public Optional<User> findByAadharNumber(String aadharNumber) {
        return users.stream().filter(u -> aadharNumber.equals(u.getAadharNumber())).findFirst();
    }

    public boolean existsByAadharNumber(String aadharNumber) {
        return users.stream().anyMatch(u -> aadharNumber.equals(u.getAadharNumber()));
    }

    public Optional<User> findById(String id) {
        return users.stream().filter(u -> id.equals(u.getId())).findFirst();
    }
}
