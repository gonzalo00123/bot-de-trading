class M5Analyzer:
    def analyze_pullbacks(self, data, h1_levels):
        """Analiza patrones de Pullback en 5M relacionados con niveles de 1H"""
        pullbacks = []
        
        for level in h1_levels:
            # Proyectar nivel 1H en datos 5M
            level_touches = self._find_level_touches(data, level['Level'])
            
            for touch in level_touches:
                # Verificar si es un pullback
                if self._is_pullback(data, touch, level):
                    # Identificar esquema (Doble, Trampa, Falla, Continuación)
                    scheme = self._identify_pullback_scheme(data, touch, level)
                    
                    pullbacks.append({
                        'level': level['Level'],
                        'level_type': level['Type'],
                        'touch_index': touch['index'],
                        'direction': 'Buy' if level['Type'] == 'Support' else 'Sell',
                        'scheme': scheme
                    })
        
        return pullbacks
    
    def analyze_ranks(self, data, h1_levels):
        """Analiza patrones de Rank en 5M relacionados con niveles de 1H"""
        ranks = []
        
        for level in h1_levels:
            # Buscar zonas de consolidación cerca del nivel
            consolidations = self._find_consolidations(data, level['Level'])
            
            for cons in consolidations:
                # Verificar si es un patrón Rank
                if self._is_rank(data, cons, level):
                    # Identificar esquema (Doble, Trampa, Falla, Continuación)
                    scheme = self._identify_rank_scheme(data, cons, level)
                    
                    # Buscar rompimiento de vela (RV)
                    rv = self._find_rv(data, cons)
                    
                    if rv:
                        ranks.append({
                            'level': level['Level'],
                            'level_type': level['Type'],
                            'consolidation_start': cons['start_index'],
                            'consolidation_end': cons['end_index'],
                            'rv_index': rv['index'],
                            'direction': rv['direction'],
                            'scheme': scheme
                        })
        
        return ranks
    
    def analyze_baston_c(self, data, h1_levels):
        """Analiza patrones de Bastón C en 5M"""
        baston_c_patterns = []
        
        for level in h1_levels:
            # Buscar retrocesos controlados al nivel
            retrocesos = self._find_controlled_retests(data, level['Level'])
            
            for retroceso in retrocesos:
                # Buscar vela gatillo (G)
                trigger = self._find_trigger_candle(data, retroceso)
                
                if trigger:
                    # Identificar esquema (Doble, Trampa, Falla, Continuación)
                    scheme = self._identify_baston_c_scheme(data, retroceso, trigger, level)
                    
                    baston_c_patterns.append({
                        'level': level['Level'],
                        'level_type': level['Type'],
                        'retroceso_index': retroceso['index'],
                        'trigger_index': trigger['index'],
                        'direction': trigger['direction'],
                        'scheme': scheme
                    })
        
        return baston_c_patterns
    
    def analyze_baston_r(self, data, h1_levels):
        """Analiza patrones de Bastón R en 5M"""
        baston_r_patterns = []
        
        for level in h1_levels:
            # Buscar toques directos al nivel con reacción inmediata
            reactions = self._find_immediate_reactions(data, level['Level'])
            
            for reaction in reactions:
                # Buscar vela gatillo (G)
                trigger = self._find_trigger_candle(data, reaction)
                
                if trigger:
                    baston_r_patterns.append({
                        'level': level['Level'],
                        'level_type': level['Type'],
                        'reaction_index': reaction['index'],
                        'trigger_index': trigger['index'],
                        'direction': 'Buy' if level['Type'] == 'Support' else 'Sell',
                        'scheme': 'BastonR'  # Bastón R es más simple, no tiene esquemas específicos
                    })
        
        return baston_r_patterns
    
    # Métodos auxiliares (implementación necesaria)
    def _find_level_touches(self, data, level_price):
        """Encuentra toques al nivel en los datos de 5M"""
        touches = []
        for i in range(len(data)):
            if abs(data['Close'][i] - level_price) < 0.0005:  # Rango ajustable
                touches.append({'index': i, 'price': data['Close'][i]})
        return touches
    
    def _is_pullback(self, data, touch, level):
        """Verifica si un toque es un pullback válido"""
        if level['Type'] == 'Resistance' and data['Low'][touch['index']] <= level['Level']:
            return True
        elif level['Type'] == 'Support' and data['High'][touch['index']] >= level['Level']:
            return True
        return False
    
    def _identify_pullback_scheme(self, data, touch, level):
        """Identifica el esquema del pullback (Doble, Trampa, Falla, Continuación)"""
        if level['Type'] == 'Resistance':
            if data['High'][touch['index']] == data['High'][touch['index'] - 2]:
                return 'Doble'
            elif data['High'][touch['index']] > data['High'][touch['index'] - 1]:
                return 'Trampa'
            elif data['High'][touch['index']] < data['High'][touch['index'] - 1]:
                return 'Falla'
            else:
                return 'Continuación'
        elif level['Type'] == 'Support':
            if data['Low'][touch['index']] == data['Low'][touch['index'] - 2]:
                return 'Doble'
            elif data['Low'][touch['index']] < data['Low'][touch['index'] - 1]:
                return 'Trampa'
            elif data['Low'][touch['index']] > data['Low'][touch['index'] - 1]:
                return 'Falla'
            else:
                return 'Continuación'
        return 'Desconocido'
    
    def _find_consolidations(self, data, level_price):
        """Encuentra consolidaciones cercanas al nivel"""
        consolidations = []
        start_index = None
        for i in range(len(data)):
            if abs(data['Close'][i] - level_price) < 0.0005:  # Rango ajustable
                if start_index is None:
                    start_index = i
            else:
                if start_index is not None:
                    consolidations.append({'start_index': start_index, 'end_index': i - 1})
                    start_index = None
        return consolidations
    
    def _is_rank(self, data, consolidation, level):
        """Verifica si una consolidación es un patrón Rank válido"""
        if consolidation['end_index'] - consolidation['start_index'] >= 3:
            return True
        return False
    
    def _identify_rank_scheme(self, data, consolidation, level):
        """Identifica el esquema del Rank (Doble, Trampa, Falla, Continuación)"""
        if level['Type'] == 'Resistance':
            if data['High'][consolidation['end_index']] == data['High'][consolidation['start_index']]:
                return 'Doble'
            elif data['High'][consolidation['end_index']] > data['High'][consolidation['start_index']]:
                return 'Trampa'
            elif data['High'][consolidation['end_index']] < data['High'][consolidation['start_index']]:
                return 'Falla'
            else:
                return 'Continuación'
        elif level['Type'] == 'Support':
            if data['Low'][consolidation['end_index']] == data['Low'][consolidation['start_index']]:
                return 'Doble'
            elif data['Low'][consolidation['end_index']] < data['Low'][consolidation['start_index']]:
                return 'Trampa'
            elif data['Low'][consolidation['end_index']] > data['Low'][consolidation['start_index']]:
                return 'Falla'
            else:
                return 'Continuación'
        return 'Desconocido'
    
    def _find_rv(self, data, consolidation):
        """Encuentra el Rompimiento de Vela (RV) después de una consolidación"""
        for i in range(consolidation['end_index'] + 1, len(data)):
            if data['Close'][i] > data['High'][consolidation['end_index']]:
                return {'index': i, 'direction': 'Buy'}
            elif data['Close'][i] < data['Low'][consolidation['end_index']]:
                return {'index': i, 'direction': 'Sell'}
        return None
    
    def _find_controlled_retests(self, data, level_price):
        """Encuentra retrocesos controlados hacia un nivel"""
        retests = []
        for i in range(len(data)):
            if abs(data['Close'][i] - level_price) < 0.0005:  # Rango ajustable
                retests.append({'index': i, 'price': data['Close'][i]})
        return retests
    
    def _find_trigger_candle(self, data, event):
        """Encuentra vela gatillo (G) que confirma la entrada"""
        for i in range(event['index'] + 1, len(data)):
            body_size = abs(data['Close'][i] - data['Open'][i])
            total_size = abs(data['High'][i] - data['Low'][i])
            body_ratio = body_size / total_size if total_size > 0 else 0

            engulfing = (data['Close'][i] > data['High'][i - 1] and data['Open'][i] < data['Low'][i - 1]) if event['direction'] == 'Buy' else \
                        (data['Close'][i] < data['Low'][i - 1] and data['Open'][i] > data['High'][i - 1])

            strong_body = body_ratio >= 0.7 and ((event['direction'] == 'Buy' and data['Close'][i] > data['Open'][i]) or 
                                                 (event['direction'] == 'Sell' and data['Close'][i] < data['Open'][i]))

            if engulfing or strong_body:
                return {'index': i, 'direction': event['direction']}
        return None
    
    def _identify_baston_c_scheme(self, data, retroceso, trigger, level):
        """Identifica el esquema de Bastón C (Doble, Trampa, Falla, Continuación)"""
        if level['Type'] == 'Resistance':
            if data['High'][retroceso['index']] == data['High'][retroceso['index'] - 2]:
                return 'Doble'
            elif data['High'][retroceso['index']] > data['High'][retroceso['index'] - 1]:
                return 'Trampa'
            elif data['High'][retroceso['index']] < data['High'][retroceso['index'] - 1]:
                return 'Falla'
            else:
                return 'Continuación'
        elif level['Type'] == 'Support':
            if data['Low'][retroceso['index']] == data['Low'][retroceso['index'] - 2]:
                return 'Doble'
            elif data['Low'][retroceso['index']] < data['Low'][retroceso['index'] - 1]:
                return 'Trampa'
            elif data['Low'][retroceso['index']] > data['Low'][retroceso['index'] - 1]:
                return 'Falla'
            else:
                return 'Continuación'
        return 'Desconocido'
    
    def _find_immediate_reactions(self, data, level_price):
        """Encuentra reacciones inmediatas en un nivel"""
        reactions = []
        for i in range(len(data)):
            if abs(data['Close'][i] - level_price) < 0.0005:  # Rango ajustable
                reactions.append({'index': i, 'price': data['Close'][i]})
        return reactions