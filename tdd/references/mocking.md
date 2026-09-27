# Quand mocker

On ne mocke qu'aux **frontières du système** :

- API externes (paiement, e-mail, etc.) ;
- bases de données (parfois ; préférer une base de test) ;
- le temps et l'aléatoire ;
- le système de fichiers (parfois).

On ne mocke pas :

- ses propres classes ou modules ;
- les collaborateurs internes ;
- tout ce qu'on contrôle.

## Concevoir pour pouvoir mocker

Aux frontières du système, préférer des interfaces faciles à remplacer.

**1. Injecter les dépendances**

Passer les dépendances externes en paramètre plutôt que de les créer à l'intérieur :

```typescript
// Facile à mocker
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Difficile à mocker
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Préférer une interface de type SDK à un « fetch » générique**

Une fonction par opération externe, plutôt qu'une fonction générique pleine de conditions :

```typescript
// BON : chaque fonction se mocke indépendamment
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// MAUVAIS : le mock doit contenir de la logique conditionnelle
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

Avec l'approche SDK :

- chaque mock renvoie une seule forme de données ;
- pas de logique conditionnelle dans la mise en place du test ;
- on voit immédiatement quels points d'accès un test utilise ;
- le typage s'applique point d'accès par point d'accès.
