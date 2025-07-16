import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        """블록체인 초기화: 빈 체인과 대기 중인 거래 리스트를 생성하고 제네시스 블록을 추가"""
        self.chain = []
        self.pending_transactions = []
        
        # 제네시스 블록(첫 번째 블록) 생성
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """제네시스 블록 생성 - 이전 해시가 없는 첫 번째 블록"""
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'nonce': 0,
            'previous_hash': '0',  # 제네시스 블록은 이전 블록이 없음
            'hash': None
        }
        
        # 제네시스 블록의 해시 계산
        genesis_block['hash'] = self.hash(genesis_block)
        self.chain.append(genesis_block)
        print("제네시스 블록이 생성되었습니다!")
    
    def new_transaction(self, sender, recipient, amount):
        """새로운 거래를 대기 리스트에 추가"""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        print(f"거래 추가: {sender} -> {recipient}: {amount}")
    
    def new_block(self, nonce):
        """새로운 블록을 생성하고 체인에 추가"""
        # 새 블록 생성
        block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transactions': self.pending_transactions,  # 대기 중인 거래들을 블록에 포함
            'nonce': nonce,
            'previous_hash': self.last_block['hash'],  # 이전 블록의 해시로 연결
            'hash': None
        }
        
        # 블록의 해시 계산
        block['hash'] = self.hash(block)
        
        # 체인에 블록 추가하고 대기 거래 리스트 초기화
        self.chain.append(block)
        self.pending_transactions = []
        
        print(f"새 블록 #{block['index']} 생성 완료! (nonce: {nonce})")
        return block
    
    @staticmethod
    def hash(block):
        """블록의 SHA-256 해시값을 계산"""
        # 해시 계산 시 hash 필드는 제외 (무한 참조 방지)
        block_copy = block.copy()
        if 'hash' in block_copy:
            del block_copy['hash']
        
        # JSON 문자열로 변환 후 해싱 (일관성 유지를 위해 정렬)
        block_string = json.dumps(block_copy, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def proof_of_work(self, last_nonce):
        """작업증명: 해시값이 '0000'으로 시작하는 nonce를 찾기"""
        nonce = 0
        print("작업증명 시작... (해시 앞 4자리가 '0000'인 nonce 찾는 중)")
        
        while True:
            # 임시 블록 생성하여 해시 확인
            temp_block = {
                'index': len(self.chain),
                'timestamp': time.time(),
                'transactions': self.pending_transactions,
                'nonce': nonce,
                'previous_hash': self.last_block['hash']
            }
            
            hash_value = self.hash(temp_block)
            
            # 해시값이 '0000'으로 시작하는지 확인 (난이도 조건)
            if hash_value.startswith('0000'):
                print(f"작업증명 완료! nonce: {nonce}, 해시: {hash_value}")
                return nonce
            
            nonce += 1
            
            # 진행 상황 출력 (매 10000번마다)
            if nonce % 10000 == 0:
                print(f"시도 횟수: {nonce}...")
    
    @property
    def last_block(self):
        """체인의 마지막 블록 반환"""
        return self.chain[-1]
    
    def display_chain(self):
        """전체 블록체인을 보기 좋게 출력"""
        print("\n" + "="*50)
        print("블록체인 전체 내용")
        print("="*50)
        
        for i, block in enumerate(self.chain):
            print(f"\n📦 블록 #{block['index']}")
            print(f"   타임스탬프: {time.ctime(block['timestamp'])}")
            print(f"   거래 수: {len(block['transactions'])}")
            
            # 거래 내용 출력
            if block['transactions']:
                print("   거래 내역:")
                for tx in block['transactions']:
                    print(f"     • {tx['sender']} -> {tx['recipient']}: {tx['amount']}")
            
            print(f"   이전 블록 해시: {block['previous_hash'][:20]}...")
            print(f"   현재 블록 해시: {block['hash'][:20]}...")
            print(f"   nonce: {block['nonce']}")
            
            # 체인 연결 시각화
            if i < len(self.chain) - 1:
                print("   ⬇️  (다음 블록과 연결)")

if __name__ == '__main__':
    print("🔗 블록체인 기본 원리 시연 🔗\n")
    
    # 1. 블록체인 객체 생성
    blockchain = Blockchain()
    
    print("\n" + "-"*40)
    print("첫 번째 블록 채굴 시작")
    print("-"*40)
    
    # 2. 첫 번째 블록용 거래 추가
    blockchain.new_transaction("Alice", "Bob", 10)
    blockchain.new_transaction("Bob", "Charlie", 5)
    
    # 3. 첫 번째 블록 채굴 (작업증명 + 블록 생성)
    nonce = blockchain.proof_of_work(blockchain.last_block['nonce'])
    blockchain.new_block(nonce)
    
    print("\n" + "-"*40)
    print("두 번째 블록 채굴 시작")
    print("-"*40)
    
    # 4. 두 번째 블록용 거래 추가
    blockchain.new_transaction("Charlie", "Dave", 3)
    blockchain.new_transaction("Dave", "Alice", 2)
    blockchain.new_transaction("Alice", "Eve", 1)
    
    # 5. 두 번째 블록 채굴
    nonce = blockchain.proof_of_work(blockchain.last_block['nonce'])
    blockchain.new_block(nonce)
    
    # 6. 완성된 블록체인 출력
    blockchain.display_chain()
    
    print("\n" + "="*50)
    print("블록체인 핵심 원리 확인:")
    print("✅ 각 블록이 이전 블록의 해시를 포함하여 '체인' 형성")
    print("✅ 작업증명을 통해 블록 생성에 계산 비용 발생")
    print("✅ 해시를 통해 블록 내용의 무결성 보장")
    print("="*50)
