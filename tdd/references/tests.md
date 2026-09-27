# Bons et mauvais tests

Les exemples sont en TypeScript, mais les principes valent pour tous les langages.

## Bons tests

**Style intégration** : on passe par les vraies interfaces, pas par des mocks des parties
internes.

```typescript
// BON : vérifie un comportement observable
test("un utilisateur peut valider un panier valide", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Caractéristiques :

- teste un comportement qui compte pour l'utilisateur ou l'appelant ;
- n'utilise que l'API publique ;
- survit aux refactorisations internes ;
- décrit le *quoi*, pas le *comment* ;
- une seule assertion logique par test.

## Mauvais tests

**Couplés à l'implémentation** : ils dépendent de la structure interne.

```typescript
// MAUVAIS : teste un détail d'implémentation
test("checkout appelle paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Signaux d'alerte :

- mock de collaborateurs internes ;
- test de fonctions privées ;
- assertions sur le nombre ou l'ordre des appels ;
- le test casse lors d'une refactorisation sans changement de comportement ;
- le nom du test décrit le *comment*, pas le *quoi* ;
- vérification par un chemin détourné plutôt que par l'interface.

```typescript
// MAUVAIS : contourne l'interface pour vérifier
test("createUser enregistre en base", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// BON : vérifie par l'interface
test("un utilisateur créé peut être relu", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Tautologiques** : la valeur attendue refait le calcul du code, donc le test passe par
construction.

```typescript
// MAUVAIS : la valeur attendue est recalculée comme le fait le code
test("calculateTotal additionne les lignes", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// BON : la valeur attendue est un littéral connu et indépendant
test("calculateTotal additionne les lignes", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
